"""Our notes (docs/*.md, docs/digest/*.md and the corrections file) as readable HTML pages, for GET /docs/<key>.

Only the pages that fif.notes publishes are served: a key is looked up in that list, never joined to a path, so
nothing else on disk can be reached. Raw HTML in the Markdown is not passed through (the digest quotes NASA files).
"""
import html
import json
import posixpath
from functools import lru_cache
from urllib.parse import urlsplit

from markdown_it import MarkdownIt

from fif import notes

STYLE = """
:root{--bg:#fbfbf9;--fg:#1d1f21;--muted:#5f6670;--line:#d9dcdf;--code:#f0f1f2;--link:#1f5fbf}
@media (prefers-color-scheme:dark){:root{--bg:#16181b;--fg:#e4e6e8;--muted:#9aa1a9;--line:#33373c;--code:#22262a;--link:#7fb0ff}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}
nav{font-size:14px;color:var(--muted);margin-bottom:16px}
a{color:var(--link)}
h1,h2,h3,h4{line-height:1.3;margin:1.6em 0 .5em}h1{margin-top:.4em}
h2{border-bottom:1px solid var(--line);padding-bottom:.2em}
code{background:var(--code);padding:.1em .3em;border-radius:3px;font-size:.9em}
pre{background:var(--code);padding:12px;overflow-x:auto;border-radius:4px}pre code{padding:0}
table{border-collapse:collapse;display:block;overflow-x:auto;font-size:14px;margin:1em 0}
th,td{border:1px solid var(--line);padding:4px 8px;vertical-align:top;text-align:left}
blockquote{margin:1em 0;padding:0 1em;color:var(--muted);border-left:3px solid var(--line)}
:target{scroll-margin-top:12px;background:color-mix(in srgb,var(--link) 12%,transparent)}
"""


def _md():
    return MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])


def _aliases():
    """Requested name -> page key: the key itself, the file's own name, with or without `.md`."""
    out = {}
    for key, path in notes.pages().items():
        stem = path.relative_to(notes.DOCS).with_suffix("").as_posix()
        for name in (key, stem):
            out[name] = out[f"{name}.md"] = key
    out[notes.CORRECTIONS_KEY] = notes.CORRECTIONS_KEY
    return out


def resolve(name):
    """Page key of a requested name, or None when it is not a published page."""
    return _aliases().get(name.strip("/"))


def _docs():
    """Path of /docs on the public address: behind a proxy that serves us under a prefix (/fuego) a bare /docs
    link would leave our pages."""
    return f"{urlsplit(notes.PUBLIC_URL).path.rstrip('/')}/docs"


def _link(href, key):
    """A relative link to another published note goes to its page; anything else is left as written."""
    if not href or "://" in href or href.startswith(("#", "/", "mailto:")):
        return href
    target, _, anchor = href.partition("#")
    if not target.endswith(".md"):
        return href
    here = posixpath.dirname(notes.pages()[key].relative_to(notes.DOCS.parent).as_posix())
    other = notes.page_key(posixpath.normpath(posixpath.join(here, target)))
    return _docs() + notes.page_url(other, anchor or None).removeprefix(f"{notes.PUBLIC_URL}/docs") if other else href


def _body(key):
    md = _md()
    tokens = md.parse(notes.pages()[key].read_text())
    seen = {}
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            anchor = notes.slug(tokens[i + 1].content)
            n = seen.get(anchor, 0)
            seen[anchor] = n + 1
            token.attrSet("id", f"{anchor}-{n}" if n else anchor)
        for child in token.children or []:
            if child.type == "link_open":
                child.attrSet("href", _link(child.attrGet("href"), key))
    return md.renderer.render(tokens, md.options, {})


def _corrections_body():
    patches = json.loads(notes.CORRECTIONS.read_text())
    out = ["<h1>Corrections to NASA's test tables</h1>",
           "<p>Every value of the PSI experiment tables that this dataset changed, filled or flagged, with its "
           "evidence. The PSI value is always kept next to the new one. Raw file: "
           f'<a href="{_docs()}/corrections.json">corrections.json</a>. How the flags are read: '
           f'<a href="{_docs()}/tests-table#flags">the tests table</a>.</p>']
    columns = ("id", "test_id", "column", "table_value", "evidence_value", "action", "evidence", "evidence_source")
    by_acc = {}
    for p in patches:
        by_acc.setdefault(p.get("accession") or "other", []).append(p)
    for acc, rows in by_acc.items():
        out.append(f'<h2 id="{html.escape(acc)}">{html.escape(acc)}</h2><table><thead><tr>'
                   + "".join(f"<th>{c}</th>" for c in columns) + "</tr></thead><tbody>")
        for p in rows:
            cells = "".join(f"<td>{html.escape('' if p.get(c) is None else str(p.get(c)))}</td>" for c in columns)
            out.append(f'<tr id="{html.escape(str(p.get("id", "")))}">{cells}</tr>')
        out.append("</tbody></table>")
    return "\n".join(out)


def _index_body():
    items = [f'<li><a href="{_docs()}/{k}">{html.escape(notes.title(k))}</a> <code>{k}</code></li>'
             for k in [*notes.pages(), notes.CORRECTIONS_KEY]]
    return ("<h1>Flame in Freefall: our notes</h1><p>How the data of the 24 NASA PSI combustion investigations were "
            "read, checked and corrected. The data functions cite these pages in their sources.</p>"
            f"<ul>{''.join(items)}</ul>")


def _page(title, body, back=True):
    nav = f'<nav><a href="{_docs()}">&larr; All notes</a></nav>' if back else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f"<title>{html.escape(title)}</title><style>{STYLE}</style></head>"
            f"<body><main>{nav}{body}</main></body></html>")


@lru_cache(maxsize=None)
def render(key):
    """The HTML page of a key returned by `resolve`, or of the index when key is None."""
    if key is None:
        return _page("Our notes", _index_body(), back=False)
    if key == notes.CORRECTIONS_KEY:
        return _page("Corrections", _corrections_body())
    return _page(notes.title(key).capitalize(), _body(key))
