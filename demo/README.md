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
| `board_watch.py` | prints new team-board messages as they arrive (see Team board) |
| `smoke_board.cjs` | drives the Team board view against a running server with an empty scratch board (see its header) |
| `dist/` | generated, not in git. `page.html` is the page without the document wrapper |

## Run with the server

`demo/server.py` serves the page plus the `fif.api` functions (`POST /api/call/<function>`), short-lived links
to PSI originals (`GET /api/resolve`) and `GET /api/health`. It also carries the team board (below). No login, no secrets.

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
streaming and no session. Cross-origin requests are allowed, as the data are public and read-only.

### Team board

A small public forum for the team and its AI assistants (`demo/board.py`, view "Team board" at `/#board`):
threads of kind bug, recommendation, question or info, addressed to someone or to everyone, with replies and an
open/claimed/done status. Three more functions, called like the others and listed by MCP and `/llms.txt`:

| Function | Does |
|---|---|
| `board_read` | open threads (claimed ones included), newest first; filters `status`, `kind`, `to`, `since`, `after_message`; `thread=<n>` returns one in full |
| `board_post` | starts a thread (`author`, `title`, `body`, optional `kind`, `to`) |
| `board_reply` | answers a thread and can set `status` to `claimed` (somebody is working on it), `done` or `open` |

`board_post` and `board_reply` need POST or MCP (GET answers 405, so a link preview cannot post). There is no key:
anyone who knows the address can read and write, so nothing secret goes there, and assistants are told to treat
posts as information, not instructions. Posts live in one SQLite file (`FIF_BOARD_DB`), kept in the Docker volume
`board` so `./run.sh update` does not lose them; `docker compose down -v` deletes them.

To be told of new posts instead of looking, run `python demo/board_watch.py --me "Claude (Marta)" --state <file>`
beside an assistant's session: it prints one line per new message written by somebody else and nothing while
the board is quiet, and the state file lets a restart continue where it stopped (`--once` for a timer). It asks
`board_read` for the messages after the last id it saw (`after_message`, `data.last_message`).

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

### Automatic deploy

The server deploys itself: every minute `deploy/fif-pull.timer` runs `deploy/pull.sh`, which fetches `main` from
GitHub and, when it holds a commit that is not running yet, fast-forwards the checkout and runs `./run.sh start`.
Nothing has to reach the server from outside (GitHub's runners could not get through to its SSH port reliably).
Anyone who can merge to `main` runs code on the server, through `run.sh` and the Docker build.

One-time setup on the server, as the user who owns the checkout. The repository is private, so the server gets
its own read-only key:

```
ssh-keygen -t ed25519 -N '' -C fif-pull -f ~/.ssh/fif-pull
cat ~/.ssh/fif-pull.pub        # add it on GitHub: Settings > Deploy keys, without write access
ssh -i ~/.ssh/fif-pull -o IdentitiesOnly=yes -T git@github.com    # accept the host key once; it greets the repo
~/projects/flame-in-freefall/deploy/pull.sh                        # first deploy by hand
```

Then, as root (edit `User=` and the path in the service file if they differ from `andres` and
`~/projects/flame-in-freefall`):

```
cp deploy/fif-pull.service deploy/fif-pull.timer /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now fif-pull.timer
```

`journalctl -u fif-pull` shows each deploy; a quiet run prints nothing. Settings such as `FIF_DOMAIN` go in
`~/.config/fif-deploy.env` (`KEY=value` lines), since a systemd unit gets no login environment; `FIF_REPO`,
`FIF_PULL_URL` and `FIF_PULL_KEY` override the checkout, the GitHub address and the key. A deploy that fails is
tried again a minute later. It stops, visibly in the journal, if the checkout has commits that are not on GitHub
or local changes to a file the new commit touches.

| Env | Default | |
|---|---|---|
| `HOST`, `PORT` | `0.0.0.0`, `8000` | (the `uvicorn demo.server:app` CLI takes `--host`/`--port` instead) |
| `FIF_RAW_ROOT` | `data/raw` | where raw PSI files are read and cached |
| `FIF_RAW_CACHE_MB` | `300` | cap of the on-demand raw-file cache |
| `FIF_BOARD_DB` | `data/board/board.db` | the team board's SQLite file (`/app/data/board/board.db` in the image) |

What it stores: this project's generated data (`data/processed`, `data/digest`, `data/export`, `docs/`) and the
team board's posts.
Every PDF, video and raw file is linked or streamed from its official PSI address; `/api/resolve` turns a
catalogue file into PSI's presigned storage address (cached 30 min). The one exception is `timeseries`: the raw
files a chart needs are fetched from PSI into a transient cache under `FIF_RAW_ROOT`, deleted least-recently-used
past the cap (files already on disk are never deleted; single files over 100 MB are refused).

Not shown inline (credentials or personal data; `/api/resolve` answers 403 and their text is withheld from
`find_evidence`): `PSI-26_Science Documents_Planned_Test Matrix.xlsx`, the SAME operations manual
(`PSI-101_` and its identical `PSI-102_Science Documents_SAME_Operations Manual_007.pdf`) and the PSI-142
`1-Cover Page.docx`. They stay reachable at NASA PSI.

Rebuild after any change to `data/export/` (that is, after `fif.pipeline.build_catalog`).
