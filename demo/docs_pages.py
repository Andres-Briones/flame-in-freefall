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

from fif import api, notes

# Same look as the Ignis app that links here (its web/src/index.css and styles.css): one dark theme, pixel titles.
# The running text is Montserrat (a font the app loads too): long notes in the pixel font were hard to read.
FONTS = ("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Montserrat:ital,wght@0,400..700;1,400..700"
         "&family=Pixelify+Sans:wght@400;600&display=swap")
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"

STYLE = """
:root{--bg:#0b080d;--surface:#140c10;--fg:#f6eee9;--muted:#bba9a6;--line:#33242a;--code:#1d1319;--link:#ffb066;
--flame:#ff5a1f;--ember:#ffc34d;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 "Montserrat",system-ui,sans-serif}
main{max-width:900px;margin:0 auto;padding:24px 16px 64px}
nav{font-size:14px;color:var(--muted);margin-bottom:16px}
a{color:var(--link)}a:hover{color:var(--ember)}
h1,h2,h3,h4{font-family:"Pixelify Sans",ui-monospace,monospace;font-weight:600;line-height:1.3;margin:1.6em 0 .5em}
h1{margin-top:.4em;color:var(--flame)}h3,h4{color:var(--ember)}
h2{color:var(--link);border-bottom:2px solid var(--line);padding-bottom:.2em}
strong{color:#ffe9d6}
code{background:var(--code);padding:.1em .3em;font:.86em "JetBrains Mono",ui-monospace,monospace}
pre{background:var(--code);border:2px solid var(--line);padding:12px;overflow-x:auto}pre code{padding:0}
table{border-collapse:collapse;display:block;overflow-x:auto;font-size:14px;margin:1em 0}
th,td{border:1px solid var(--line);padding:4px 8px;vertical-align:top;text-align:left}
th{font-family:"Pixelify Sans",ui-monospace,monospace;color:var(--ember);background:var(--surface)}
blockquote{margin:1em 0;padding:0 1em;color:var(--muted);border-left:4px solid var(--flame)}
:target{scroll-margin-top:12px;background:color-mix(in srgb,var(--link) 14%,transparent)}
.math.display{display:block;overflow-x:auto;overflow-y:hidden;padding:4px 0}
.katex{font-size:1.1em}
"""

# The formulas stay as TeX in the page and KaTeX draws them in the browser; without it the TeX is still readable.
MATH_SCRIPT = """
addEventListener("DOMContentLoaded",function(){if(!window.katex)return;
document.querySelectorAll(".math").forEach(function(e){try{katex.render(e.textContent,e,
{displayMode:e.classList.contains("display"),throwOnError:false})}catch(_){}})});
"""


def _math(state, silent):
    """Inline rule for `$...$` and `$$...$$`: the TeX is kept as written (Markdown would eat its backslashes).
    A single `$` opens a formula only when it hugs its content and the closing one is not followed by a digit, so
    amounts of money are left alone."""
    src, pos = state.src, state.pos
    if src[pos] != "$":
        return False
    display = src.startswith("$$", pos)
    start = pos + (2 if display else 1)
    end = src.find("$$" if display else "$", start)
    if end <= start:
        return False
    tex = src[start:end]
    if not display and (tex != tex.strip() or "\n" in tex or src[end + 1:end + 2].isdigit()):
        return False
    if not silent:
        token = state.push("math", "span", 0)
        token.content = tex.strip()
        token.meta = {"display": display}
    state.pos = end + (2 if display else 1)
    return True


def _render_math(self, tokens, idx, options, env):
    token = tokens[idx]
    return f'<span class="math{" display" if token.meta["display"] else ""}">{html.escape(token.content)}</span>'


def _md():
    md = MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])
    md.inline.ruler.before("escape", "math", _math)
    md.add_render_rule("math", _render_math)
    return md


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
           "<p>The values of the PSI experiment tables that this dataset changed, filled or flagged. First, by "
           "investigation, the disagreements with the raw sensor data, each with its evidence (raw file: "
           f'<a href="{_docs()}/corrections.json">corrections.json</a>). Then '
           '<a href="#values-changed">every value of the tests table that differs from PSI\'s</a>, whatever the '
           "reason (the raw data, the reports or a rule of the build; the row's flags say which). The PSI value is "
           "always kept next to the new one. How the flags are read: "
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
    columns = ("accession", "test_id", "column", "table_value", "value_now", "flags", "patch_ids")
    out.append('<h2 id="values-changed">Every value changed in the tests table</h2><table><thead><tr>'
               + "".join(f"<th>{c}</th>" for c in columns) + "</tr></thead><tbody>")
    for c in api.values_changed(api.table("tests")):
        cells = "".join(f"<td>{html.escape('' if c.get(k) is None else str(c.get(k)))}</td>" for k in columns)
        # Investigations without raw-data conflicts get their anchor (a source's #accession) on their first row here.
        anchor = c["accession"] not in by_acc and f' id="{html.escape(c["accession"])}"'
        by_acc.setdefault(c["accession"], [])
        out.append(f"<tr{anchor or ''}>{cells}</tr>")
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
    math = (f'<link rel="stylesheet" href="{KATEX}/katex.min.css"><script defer src="{KATEX}/katex.min.js"></script>'
            f"<script>{MATH_SCRIPT}</script>") if 'class="math' in body else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)}</title><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{STYLE}</style>{math}</head>'
            f"<body><main>{nav}{body}</main></body></html>")


@lru_cache(maxsize=None)
def render(key):
    """The HTML page of a key returned by `resolve`, or of the index when key is None."""
    if key is None:
        return _page("Our notes", _index_body(), back=False)
    if key == notes.CORRECTIONS_KEY:
        return _page("Corrections", _corrections_body())
    return _page(notes.title(key).capitalize(), _body(key))
