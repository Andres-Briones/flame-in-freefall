"""Small backend for the dashboard demo: the `fif.api` functions over HTTP, short-lived links to PSI originals,
and the built page from demo/dist/.

    uv run --group server uvicorn demo.server:app --port 8000      (or: uv run --group server python demo/server.py)

It stores nothing from NASA except this project's own generated data (data/processed, data/digest, data/export).
PSI originals are linked or streamed from PSI's storage; the only exception is the transient raw-file cache that
`timeseries` needs (see RawCache).

Env: HOST (0.0.0.0), PORT (8000), FIF_RAW_CACHE_MB (300), FIF_RAW_ROOT (where raw files are read and cached;
default data/raw).
"""
import csv
import json
import math
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, Request  # noqa: E402
from fastapi.concurrency import run_in_threadpool  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.middleware.gzip import GZipMiddleware  # noqa: E402
from fastapi.responses import JSONResponse, PlainTextResponse, Response  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from fif import api, psi  # noqa: E402
from fif.tools import TOOLS  # noqa: E402

DIST = ROOT / "demo" / "dist"
PSI_BASE = "https://psi.nasa.gov/geode-py/ws/studies"
USER_AGENT = "Mozilla/5.0"
PSI_TIMEOUT_S = 10
RESOLVE_TTL_S = 30 * 60
RESOLVE_CACHE_SIZE = 2000
S3_DEFAULT_EXPIRES_S = 7200
MAX_RAW_FILE_BYTES = 100 * 1024 * 1024
DATA_MAX_AGE_S = 300

# These PSI files contain credentials or personal data (rule in docs/digest/AUTHORING.md), so the server never
# resolves them for inline viewing and never returns their extracted text. The PSI-102 manual is a byte-identical
# copy of the PSI-101 one. The PSI-142 cover page is a removed legacy file, not in files.csv.
NOT_INLINE = frozenset({
    ("PSI-26", "PSI-26_Science Documents_Planned_Test Matrix.xlsx"),
    ("PSI-101", "PSI-101_Science Documents_SAME_Operations Manual_007.pdf"),
    ("PSI-102", "PSI-102_Science Documents_SAME_Operations Manual_007.pdf"),
    ("PSI-142", "1-Cover Page.docx"),
})
NOT_INLINE_DETAIL = "Not shown inline; open it at NASA PSI."

# Upper bounds on size-like arguments, so one request cannot ask for an unbounded answer.
ARG_CAPS = {
    "filter_tests": {"limit": 3000},
    "find_evidence": {"k": 50},
    "timeseries": {"max_points": 5000},
    "search_investigations": {"limit": 200},
    "relevance": {"top": 200},
}


def _load_catalogue():
    with open(psi.PROCESSED / "files.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    return {(r["accession"], r["file_name"]): {"size": int(float(r["size_bytes"] or 0)), "local_path": r["local_path"],
                                               "dead": r.get("status") == "dead_link"}
            for r in rows}


CATALOGUE = _load_catalogue()
BY_LOCAL_PATH = {v["local_path"]: k for k, v in CATALOGUE.items()}


# --- resolving PSI addresses ------------------------------------------------------------------------------

class PsiGone(Exception):
    """PSI answered 404 for a catalogue file."""


class PsiFailed(Exception):
    """PSI did not answer with a usable redirect."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def psi_address(accession, file_name):
    return f"{PSI_BASE}/{accession}/download?" + urllib.parse.urlencode({"file": file_name}, quote_via=urllib.parse.quote)


def psi_redirect(url):
    """(status, Location) of a PSI download address, without following the redirect."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with _opener.open(req, timeout=PSI_TIMEOUT_S) as r:
            return r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location")


def _s3_expiry(location):
    query = urllib.parse.parse_qs(urllib.parse.urlparse(location).query)
    try:
        return int(query.get("X-Amz-Expires", [S3_DEFAULT_EXPIRES_S])[0])
    except ValueError:
        return S3_DEFAULT_EXPIRES_S


_resolved = OrderedDict()  # (accession, file_name) -> (url, issued_at, expires_s)
_resolved_lock = threading.Lock()


def resolve_file(accession, file_name):
    """Presigned storage address of a catalogue file: {"url", "expires_in_s"}. Raises PsiGone or PsiFailed."""
    key = (accession, file_name)
    now = time.time()
    with _resolved_lock:
        hit = _resolved.get(key)
        if hit and now - hit[1] < RESOLVE_TTL_S:
            _resolved.move_to_end(key)
            return {"url": hit[0], "expires_in_s": int(hit[1] + hit[2] - now)}
    try:
        status, location = psi_redirect(psi_address(accession, file_name))
    except (OSError, ValueError) as e:  # timeouts and connection errors are OSError
        raise PsiFailed(f"PSI did not answer: {type(e).__name__}") from e
    if status == 404:
        raise PsiGone("PSI no longer serves this file")
    if status not in (301, 302, 303, 307, 308) or not location:
        raise PsiFailed(f"PSI answered {status} without a redirect")
    parsed = urllib.parse.urlparse(location)
    if parsed.scheme != "https" or not (parsed.hostname or "").endswith(".amazonaws.com"):
        raise PsiFailed("PSI redirected to an unexpected host")
    expires = _s3_expiry(location)
    with _resolved_lock:
        _resolved[key] = (location, now, expires)
        _resolved.move_to_end(key)
        while len(_resolved) > RESOLVE_CACHE_SIZE:
            _resolved.popitem(last=False)
    return {"url": location, "expires_in_s": expires}


# --- transient raw-file cache for timeseries --------------------------------------------------------------

def download_from_psi(accession, file_name, dest):
    """Stream a catalogue file from PSI storage to `dest` (via a .part file), refusing more than MAX_RAW_FILE_BYTES."""
    url = resolve_file(accession, file_name)["url"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as r, open(part, "wb") as out:
            n = 0
            while chunk := r.read(1 << 20):
                n += len(chunk)
                if n > MAX_RAW_FILE_BYTES:
                    raise PsiFailed("file larger than the server's limit")
                out.write(chunk)
        part.replace(dest)
    except OSError as e:
        raise PsiFailed(f"download failed: {type(e).__name__}") from e
    finally:
        part.unlink(missing_ok=True)


class RawCache:
    """On-demand copies of the raw PSI files a `timeseries` call reads. This is a transient cache, not storage:
    files are fetched from PSI when a chart needs them and deleted least-recently-used first once the total passes
    `cap_bytes`. Only files this cache downloaded are ever deleted (listed in `<root>/.server_cache.json`, so a
    restart keeps track of them); files that were already on disk, such as a developer's full raw copy, are never
    touched."""

    def __init__(self, root, cap_bytes, fetch=download_from_psi):
        self.root = Path(root)
        self.cap = cap_bytes
        self.fetch = fetch
        self.index = self.root / ".server_cache.json"
        self.lock = threading.Lock()
        self.file_locks = {}
        self.owned = OrderedDict()  # absolute path -> size, least recently used first
        try:
            for path, size in json.loads(self.index.read_text()):
                if Path(path).exists():
                    self.owned[path] = size
        except (OSError, ValueError, TypeError):
            pass

    def _save(self):
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            self.index.write_text(json.dumps(list(self.owned.items())))
        except OSError:
            pass

    def ensure(self, accession, file_name, dest, size, keep=()):
        """Make `dest` exist, downloading it if missing. `keep` are paths the caller is about to read."""
        dest = Path(dest)
        key = str(dest)
        if dest.exists():
            with self.lock:
                if key in self.owned:
                    self.owned.move_to_end(key)
            return
        if size > MAX_RAW_FILE_BYTES:
            raise ValueError(f"{file_name} is {size / 1e6:.0f} MB, over the server's {MAX_RAW_FILE_BYTES // 2**20} MB "
                             "limit; download it from NASA PSI")
        with self.lock:
            file_lock = self.file_locks.setdefault(key, threading.Lock())
        with file_lock:
            if not dest.exists():
                self.fetch(accession, file_name, dest)
                with self.lock:
                    self.owned[key] = dest.stat().st_size
                    self.owned.move_to_end(key)
        self.evict(keep={key, *map(str, keep)})

    def evict(self, keep=()):
        """Delete least-recently-used downloaded files until the total is under the cap; never files in `keep`."""
        with self.lock:
            for key in list(self.owned):
                if sum(self.owned.values()) <= self.cap:
                    break
                if key in keep:
                    continue
                Path(key).unlink(missing_ok=True)
                del self.owned[key]
                self.file_locks.pop(key, None)
            self._save()


raw_cache = RawCache(psi.RAW, int(float(os.environ.get("FIF_RAW_CACHE_MB", "300")) * 2**20))


def timeseries_files(test_id, test_point=None, accession=None, **_):
    """Catalogue keys of the raw files `api.timeseries` will read for these arguments (same selection rules),
    including companion files the readers open (CFI chamber readings)."""
    feats = api.table("timeseries_features")
    key = str(test_id).replace(" ", "")
    sel = feats[(feats["test_id"].str.replace(" ", "") == key) | (feats["test_point"] == key)]
    if test_point is not None:
        sel = sel[sel["test_point"] == test_point]
    if accession is not None:
        sel = sel[sel["accession"] == api._accession(accession)]
    if sel.empty or sel["accession"].nunique() > 1:
        return []  # api.timeseries raises the explanatory error
    row = sel.iloc[0]
    sources = feats.loc[(feats["accession"] == row["accession"]) & (feats["test_point"] == row["test_point"]),
                        "source_file"]
    paths = []
    for source in sources:
        paths.append(source)
        if "_Radiometer_Readings" in source:
            paths.append(source.replace("_Radiometer_Readings", "_Chamber_Readings"))
    return [BY_LOCAL_PATH[p] for p in paths if p in BY_LOCAL_PATH]


def prefetch_timeseries(kwargs):
    keys = timeseries_files(**kwargs)
    dests = [psi.raw_file(CATALOGUE[k]["local_path"]) for k in keys]
    for (acc, name), dest in zip(keys, dests):
        raw_cache.ensure(acc, name, dest, CATALOGUE[(acc, name)]["size"], keep=dests)


# --- calling fif.api --------------------------------------------------------------------------------------

def _plain(value):
    """JSON-safe copy: numpy scalars to Python, NaN and infinities to None."""
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            value = value.item()
        except (TypeError, ValueError):
            pass
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _withhold_not_inline(result):
    data = result.get("data") or {}
    docs = data.get("documents") or []
    kept = [d for d in docs if (d.get("accession"), d.get("file_name")) not in NOT_INLINE]
    if len(kept) < len(docs):
        data["documents"] = kept
        result["sources"] = [s for s in result.get("sources", []) if (s.get("accession"), s.get("file")) not in NOT_INLINE]
        result["notes"] = [*result.get("notes", []),
                           "Passages from PSI files that contain credentials or personal data are not returned."]
    return result


def call_function(name, kwargs):
    fn = api.FUNCTIONS[name]
    for arg, cap in ARG_CAPS.get(name, {}).items():
        if arg in kwargs:
            if not isinstance(kwargs[arg], int) or isinstance(kwargs[arg], bool) or kwargs[arg] < 1:
                raise ValueError(f"{arg} must be a positive integer")
            kwargs[arg] = min(kwargs[arg], cap)
    if name == "timeseries":
        prefetch_timeseries(kwargs)
    result = fn(**kwargs)
    if name == "find_evidence":
        result = _withhold_not_inline(result)
    return json.dumps(_plain(result), allow_nan=False, default=str, ensure_ascii=False)


# --- app --------------------------------------------------------------------------------------------------

app = FastAPI(title="Flame in Freefall demo", docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(GZipMiddleware, minimum_size=1000)
# The data are public and read-only, and AI tools running in a browser call from other origins.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])


@app.middleware("http")
async def cache_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/data/") and response.status_code == 200:
        response.headers["Cache-Control"] = f"public, max-age={DATA_MAX_AGE_S}"
    elif request.url.path.startswith(("/api", "/mcp", "/llms.txt", "/openapi.json")):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/api/health")
def health():
    return {"ok": True, "functions": list(api.FUNCTIONS), "raw_on_disk": (psi.RAW / "investigations").is_dir()}


@app.get("/api/resolve")
def resolve(accession: str, file: str):
    if (accession, file) in NOT_INLINE:
        raise HTTPException(403, NOT_INLINE_DETAIL)
    if (accession, file) not in CATALOGUE:
        raise HTTPException(404, "Not a file of the PSI catalogue")
    if CATALOGUE[(accession, file)]["dead"]:
        raise HTTPException(404, "PSI lists this file but its storage link is dead (data/corrections/files_status.json)")
    try:
        return resolve_file(accession, file)
    except PsiGone as e:
        raise HTTPException(404, str(e))
    except PsiFailed as e:
        raise HTTPException(502, str(e))


async def run_function(function, kwargs):
    """Call one fif.api function; failures become HTTP errors whose detail says what to change."""
    if function not in api.FUNCTIONS:
        raise HTTPException(404, f"Unknown function {function!r}; available: {', '.join(api.FUNCTIONS)}")
    if not isinstance(kwargs, dict):
        raise HTTPException(400, "The arguments must be a JSON object of keyword arguments")
    try:
        return await run_in_threadpool(call_function, function, kwargs)
    except PsiGone:
        raise HTTPException(404, "A raw file this needs is no longer served by PSI")
    except PsiFailed as e:
        raise HTTPException(502, f"Could not fetch a raw file from PSI: {e}")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
        detail = e.args[0] if isinstance(e, KeyError) and e.args else str(e)
        raise HTTPException(400, f"{type(e).__name__}: {detail}")


@app.post("/api/call/{function}")
async def call(function: str, request: Request):
    try:
        body = await request.body()
        kwargs = json.loads(body) if body.strip() else {}
    except ValueError:
        raise HTTPException(400, "The request body must be a JSON object of keyword arguments")
    return Response(await run_function(function, kwargs), media_type="application/json")


# --- for AI agents: GET calls, a plain-text guide, tool specs, OpenAPI, MCP -------------------------------------

TOOL_BY_NAME = {t["name"]: t for t in TOOLS}
MCP_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
SUMMARY = ("Flame in Freefall: the 24 NASA PSI microgravity combustion investigations (2,177 tests, sensor traces, "
           "document evidence, reviewed findings, fire-safety relevance, data-quality patches) as 11 read-only "
           "functions. Every answer is {data, chart, sources, notes}: cite `sources`, and pass on `notes`, which "
           "carry the caveats.")


def query_arguments(function, params):
    """Keyword arguments from a query string: `args=<JSON object>`, or one parameter per argument, where anything
    the tool schema does not type as a plain string is read as JSON (x_o2=[0.18,0.21], limit=20, flight=true)."""
    if "args" in params:
        try:
            return json.loads(params["args"])
        except ValueError:
            raise HTTPException(400, "args must be a URL-encoded JSON object")
    properties = TOOL_BY_NAME.get(function, {}).get("input_schema", {}).get("properties", {})
    kwargs = {}
    for key, text in params.items():
        types = properties.get(key, {}).get("type", "string")
        types = [types] if isinstance(types, str) else types
        if types == ["string"]:
            kwargs[key] = text
            continue
        try:
            kwargs[key] = json.loads(text)
        except ValueError:
            if "string" not in types:
                raise HTTPException(400, f"{key} must be JSON of type {' or '.join(map(str, types))}, got {text!r}")
            kwargs[key] = text
    return kwargs


@app.get("/api/call/{function}")
async def call_get(function: str, request: Request):
    """The same call for clients that can only fetch a URL."""
    if function not in api.FUNCTIONS:
        raise HTTPException(404, f"Unknown function {function!r}; available: {', '.join(api.FUNCTIONS)}")
    return Response(await run_function(function, query_arguments(function, dict(request.query_params))),
                    media_type="application/json")


def _base(request):
    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    return f"{proto}://{request.headers.get('host') or request.url.netloc}"


@app.get("/api")
@app.get("/api/tools")
def tools(request: Request):
    base = _base(request)
    return {"about": SUMMARY, "guide": f"{base}/llms.txt", "openapi": f"{base}/openapi.json", "mcp": f"{base}/mcp",
            "call": f"POST {base}/api/call/<name> with a JSON object of arguments, or GET with query parameters",
            "tools": TOOLS}


def _example(tool):
    props = tool["input_schema"]["properties"]
    args = {k: EXAMPLE_VALUES.get(k, "...") for k in tool["input_schema"]["required"]}
    for k in EXAMPLE_OPTIONAL.get(tool["name"], ()):
        if k in props:
            args[k] = EXAMPLE_VALUES[k]
    return args


EXAMPLE_VALUES = {"accession": "PSI-25", "accessions": ["PSI-25", "PSI-26"], "scenario": "moon-habitat",
                  "fuel_phase": "solid", "query": "flame spread over PMMA", "question": "flammability limit of PMMA",
                  "x_o2": [0.18, 0.21], "limit": 20, "k": 5, "model": "cfig_normal_self_extinction",
                  "test_id": "22024M1"}
EXAMPLE_OPTIONAL = {"search_investigations": ("query", "fuel_phase"), "filter_tests": ("accession", "x_o2", "limit"),
                    "find_evidence": ("k",), "relevance": ("fuel_phase",)}


def _describe(name, spec):
    types = spec.get("type", "any")
    kind = " or ".join(map(str, types)) if isinstance(types, list) else str(types)
    if spec.get("enum"):
        kind += ", one of " + " | ".join(str(v) for v in spec["enum"] if v is not None)
    return f"  - {name} ({kind})" + (f": {spec['description']}" if spec.get("description") else "")


@app.get("/llms.txt", response_class=PlainTextResponse)
def guide(request: Request):
    base = _base(request)
    out = ["# Flame in Freefall data API", "", SUMMARY, "",
           "## How to call", "",
           f"- POST {base}/api/call/<function> with a JSON object of arguments (an empty body means no arguments).",
           f"- GET {base}/api/call/<function>?name=value for clients that can only fetch a URL. Numbers, booleans,",
           "  lists and ranges are written as JSON (x_o2=[0.18,0.21], flight=true); or pass everything as",
           "  args=<URL-encoded JSON object>.",
           f"- MCP (streamable HTTP, no login): {base}/mcp, for example `claude mcp add --transport http fif {base}/mcp`.",
           f"- Tool definitions as JSON Schema: {base}/api/tools. OpenAPI 3.1: {base}/openapi.json.",
           "- No key is needed. Everything is read-only. Errors are JSON {\"detail\": \"...\"} with status 400 (bad",
           "  argument, the detail says which), 404 (unknown function or file) or 502 (NASA storage did not answer).",
           "", "## Good habits", "",
           "- Start with search_investigations or relevance, then narrow with get_investigation, filter_tests,",
           "  find_evidence. Investigations are named by accession (PSI-25) or acronym (BASS).",
           "- Answers can be large (get_investigation and filter_tests reach 100 kB): use `limit`, `k`, `top` and",
           "  filters. `chart` is a plotting hint and can be ignored.",
           "- `notes` state caveats and doubts about the source data: repeat the relevant ones in your answer.",
           "- Rows of the tests table carry `flags`; call discrepancies before relying on a flagged value.",
           "- predict refuses conditions outside what was tested; report the refusal, do not extrapolate.",
           f"- A file named in `sources` opens at {base}/api/resolve?accession=PSI-25&file=<file name>, which returns",
           "  a short-lived NASA storage link.",
           "", "## Functions", ""]
    for tool in TOOLS:
        schema = tool["input_schema"]
        out += [f"### {tool['name']}", "", tool["description"], ""]
        if schema["properties"]:
            required = set(schema["required"])
            out += ["Arguments" + (f" (required: {', '.join(schema['required'])})" if required else " (all optional)") + ":"]
            out += [_describe(k, v) for k, v in schema["properties"].items()]
        else:
            out += ["No arguments."]
        args = _example(tool)
        body = json.dumps(args, ensure_ascii=False)
        query = urllib.parse.urlencode({k: v if isinstance(v, str) else json.dumps(v, separators=(",", ":"))
                                        for k, v in args.items()})
        out += ["", f"    curl -X POST {base}/api/call/{tool['name']} -d '{body}'",
                f"    GET {base}/api/call/{tool['name']}" + (f"?{query}" if query else ""), ""]
    return "\n".join(out)


@app.get("/openapi.json")
def openapi(request: Request):
    paths = {}
    for tool in TOOLS:
        paths[f"/api/call/{tool['name']}"] = {"post": {
            "operationId": tool["name"], "summary": tool["description"][:120], "description": tool["description"],
            "requestBody": {"required": bool(tool["input_schema"]["required"]),
                            "content": {"application/json": {"schema": tool["input_schema"]}}},
            "responses": {"200": {"description": "{data, chart, sources, notes}",
                                  "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Answer"}}}},
                          "400": {"description": "Bad argument; `detail` says which"}}}}
    return {"openapi": "3.1.0", "info": {"title": "Flame in Freefall data API", "version": "1", "description": SUMMARY},
            "servers": [{"url": _base(request)}], "paths": paths,
            "components": {"schemas": {"Answer": {"type": "object", "properties": {
                "data": {"type": "object"}, "chart": {"type": ["object", "null"]},
                "sources": {"type": "array", "items": {"type": "object"}},
                "notes": {"type": "array", "items": {"type": "string"}}}}}}}


async def _mcp_result(method, params):
    if method == "initialize":
        asked = params.get("protocolVersion")
        return {"protocolVersion": asked if asked in MCP_VERSIONS else MCP_VERSIONS[0],
                "capabilities": {"tools": {}}, "serverInfo": {"name": "flame-in-freefall", "version": "1"},
                "instructions": SUMMARY}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{"name": t["name"], "description": t["description"], "inputSchema": t["input_schema"],
                           "annotations": {"readOnlyHint": True}} for t in TOOLS]}
    if method == "tools/call":
        try:
            text = await run_function(params.get("name"), params.get("arguments") or {})
        except HTTPException as e:
            return {"content": [{"type": "text", "text": str(e.detail)}], "isError": True}
        return {"content": [{"type": "text", "text": text}]}
    raise LookupError(method)


@app.post("/mcp")
async def mcp(request: Request):
    """Model Context Protocol over streamable HTTP, stateless: one JSON-RPC message in, one JSON answer out."""
    try:
        message = json.loads(await request.body())
        method = message["method"]
    except (ValueError, KeyError, TypeError):
        return JSONResponse({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Expected one JSON-RPC request"}}, 400)
    if "id" not in message:
        return Response(status_code=202)
    try:
        params = message.get("params")
        result = await _mcp_result(method, params if isinstance(params, dict) else {})
    except LookupError:
        return JSONResponse({"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": f"Method not found: {method}"}})
    return JSONResponse({"jsonrpc": "2.0", "id": message["id"], "result": result})


@app.get("/mcp")
def mcp_no_stream():
    return Response(status_code=405, headers={"Allow": "POST"})


app.mount("/", StaticFiles(directory=DIST, html=True, check_dir=False), name="dist")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", "8000")))
