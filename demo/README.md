# Dashboard capability demo

A static page that shows, on the real data, what the science side needs from the final dashboard. It is a
prototype for discussion, not the product. Every view has a "For the dashboard team" button that names the data
file, the `fif.api` call and the caveats that must stay on screen; the Brief view collects them.

```
uv run python demo/build_demo.py      # writes demo/dist/
open demo/dist/index.html             # works from disk; charts and fonts need internet (cdnjs, Google Fonts)
```

| Path | Content |
|---|---|
| `build_demo.py` | trims `data/export/*.json` into `dist/data/*.js` and inlines `src/` into one page |
| `src/core.js` | router and helpers; its header comment is the API for views |
| `src/views/<id>.js` | one file per view |
| `smoke.cjs` | draws every view in jsdom and fails on errors: `NODE_PATH=<jsdom>/node_modules node demo/smoke.cjs` |
| `dist/` | generated, not in git. `page.html` is the page without the document wrapper |

## Run with the server

`demo/server.py` serves the page plus the `fif.api` functions (`POST /api/call/<function>`), short-lived links
to PSI originals (`GET /api/resolve`) and `GET /api/health`. No login, no secrets.

### For AI agents

Give a teammate's AI the address `<server>/llms.txt`: a plain-text guide, generated from `fif/tools.py`, with every
function, its arguments and a working example. The same functions are reachable four ways:

| Client | Use |
|---|---|
| can only fetch a URL | `GET /api/call/<function>?accession=PSI-25&x_o2=[0.18,0.21]` (non-string values as JSON, or `args=<JSON>`) |
| can send HTTP | `POST /api/call/<function>` with a JSON object |
| Claude Code, Claude Desktop, other MCP clients | `claude mcp add --transport http fif <server>/mcp` |
| function calling, custom GPT actions | tool schemas at `/api/tools`, OpenAPI 3.1 at `/openapi.json` |

The MCP endpoint is stateless JSON-RPC over POST (`initialize`, `tools/list`, `tools/call`, `ping`); it has no
streaming and no session. Cross-origin requests are allowed, as everything is public and read-only.

```
uv run python demo/build_demo.py && uv run python demo/server.py        # http://localhost:8000
docker compose up -d --build                                             # same, from the repo root
```

On a server, use `./run.sh` from the repo root: it builds and starts the container on port 5187 (`FIF_PORT`),
refuses if another process holds that port, and waits for `/api/health`. `./run.sh update` pulls and restarts;
`stop`, `restart`, `logs`, `status` do what they say. Behind nginx or Caddy, run it with `FIF_BIND=127.0.0.1`.
`FIF_DOMAIN=<dns name of the host> ./run.sh` also starts Caddy on ports 80/443 with a Let's Encrypt certificate
(`demo/compose.https.yml`), for browsers that refuse plain HTTP on the domain; `./run.sh logs caddy` shows it.
It uses host networking (`demo/compose.host.yml`): ports published through Docker were refused from outside on
the production server while direct listeners passed. `FIF_NETWORK=bridge ./run.sh` uses published ports instead.

| Env | Default | |
|---|---|---|
| `HOST`, `PORT` | `0.0.0.0`, `8000` | (the `uvicorn demo.server:app` CLI takes `--host`/`--port` instead) |
| `FIF_RAW_ROOT` | `data/raw` | where raw PSI files are read and cached |
| `FIF_RAW_CACHE_MB` | `300` | cap of the on-demand raw-file cache |

What it stores: only this project's generated data (`data/processed`, `data/digest`, `data/export`, `docs/`).
Every PDF, video and raw file is linked or streamed from its official PSI address; `/api/resolve` turns a
catalogue file into PSI's presigned storage address (cached 30 min). The one exception is `timeseries`: the raw
files a chart needs are fetched from PSI into a transient cache under `FIF_RAW_ROOT`, deleted least-recently-used
past the cap (files already on disk are never deleted; single files over 100 MB are refused).

Not shown inline (credentials or personal data; `/api/resolve` answers 403 and their text is withheld from
`find_evidence`): `PSI-26_Science Documents_Planned_Test Matrix.xlsx`, the SAME operations manual
(`PSI-101_` and its identical `PSI-102_Science Documents_SAME_Operations Manual_007.pdf`) and the PSI-142
`1-Cover Page.docx`. They stay reachable at NASA PSI.

Rebuild after any change to `data/export/` (that is, after `fif.pipeline.build_catalog`).
