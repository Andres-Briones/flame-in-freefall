"""Watch the team board: print one line for each new message that somebody else wrote, and nothing while the board
is quiet. Meant to run beside an AI assistant's session (each line wakes the assistant), or from a timer with --once.

    python demo/board_watch.py --me "Claude (Andres)" --state ~/.board-watch.json

The state file keeps the id of the last message seen, so a restart neither repeats nor misses messages. The first
run with a new state file starts from the present; --from-start prints the whole board instead. It follows the
server's live event stream (/api/board/events) and falls back to polling board_read every --interval seconds when
the server has no stream or the connection fails; --once and --poll only poll. Standard library only, so it runs
without the project's environment.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_BASE = "http://www.open-poker.ch:5187"


def http_read(base):
    def read(**args):
        query = urllib.parse.urlencode({k: json.dumps(v) if not isinstance(v, str) else v for k, v in args.items()})
        with urllib.request.urlopen(f"{base.rstrip('/')}/api/call/board_read?{query}", timeout=30) as r:
            return json.load(r)["data"]
    return read


class NoStream(Exception):
    """The server has no event stream (an older deploy)."""


def http_events(base):
    def events(after_message):
        """Event dicts from the server's stream, after `after_message`, until the connection ends."""
        url = f"{base.rstrip('/')}/api/board/events?after_message={after_message}"
        try:
            # the server sends a keepalive every 20 s, so a minute of silence means a dead connection
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "text/event-stream"}), timeout=60)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise NoStream() from e
            raise
        with r:
            data = []
            for raw in r:
                line = raw.decode("utf-8").rstrip("\r\n")
                if not line:
                    if data:
                        yield json.loads("\n".join(data))
                    data = []
                elif line.startswith("data:"):
                    data.append(line[5:].removeprefix(" "))
    return events


MARKS = {"verified": "verified", "other_key": "OTHER KEY", "unsigned": "unsigned"}


def _mark(message):
    mark = MARKS.get(message.get("signature"))
    return f" [{mark}]" if mark else ""


def check(read, state_path, me, from_start=False):
    """Lines for the messages newer than the saved cursor that `me` did not write; moves the cursor."""
    state_path = Path(state_path)
    cursor = json.loads(state_path.read_text())["last_message"] if state_path.exists() else None
    if cursor is None and not from_start:
        cursor, lines = read(limit=1)["last_message"], []
    else:
        data = read(status="all", after_message=cursor or 0, limit=200)
        cursor, lines = data["last_message"], []
        for t in sorted(data["threads"], key=lambda t: t["thread"]):
            for m in t["new_messages"]:
                if m["author"].casefold() == me.casefold() or m["id"] > cursor:
                    continue
                lines.append(_line(t, m))
    _save(state_path, cursor)
    return lines


def _line(t, m):
    body = " ".join(m["body"].split())
    return (f"thread {t['thread']} [{t['kind']}, {t['status']}, for {t['to']}] \"{t['title']}\" "
            f"message {m['id']} from {m['author']}{_mark(m)}: {body[:300]}")


def _save(state_path, cursor):
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps({"last_message": cursor}))


def follow(events, read, state_path, me, emit):
    """Emit a line for each streamed message that `me` did not write (its body read with board_read), moving the
    cursor after each one. Returns when the stream ends."""
    state_path = Path(state_path)
    for event in events(json.loads(state_path.read_text())["last_message"]):
        if event["author"].casefold() != me.casefold():
            t = read(thread=event["thread"])["thread"]
            emit(_line(t, next(m for m in t["messages"] if m["id"] == event["id"])))
        _save(state_path, event["id"])


def watch(read, events, state_path, me, emit, interval, from_start=False, sleep=time.sleep):
    """Catch up by polling, then follow the stream; poll every `interval` seconds instead while the stream is
    missing (`events` None or the server answers 404) or broken."""
    while True:
        try:
            for line in check(read, state_path, me, from_start):
                emit(line)
            if events is not None:
                follow(events, read, state_path, me, emit)
                sleep(2)  # the stream ended, as in a server restart: catch up and reconnect
                continue
        except NoStream:
            print("board_watch: the server has no event stream; polling", file=sys.stderr, flush=True)
            events = None
            continue
        except (OSError, ValueError, KeyError) as e:
            # a server restart during a deploy must not end the watch
            print(f"board_watch: {e}", file=sys.stderr, flush=True)
        sleep(interval)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--me", required=True, help="your signature on the board; your own messages are not reported")
    p.add_argument("--state", required=True, help="file that remembers the last message seen")
    p.add_argument("--base", default=DEFAULT_BASE)
    p.add_argument("--interval", type=float, default=45, help="seconds between checks")
    p.add_argument("--once", action="store_true", help="check once and exit")
    p.add_argument("--from-start", action="store_true", help="with a new state file, report the whole board")
    p.add_argument("--poll", action="store_true", help="poll every --interval seconds instead of following the stream")
    a = p.parse_args()
    read, state = http_read(a.base), Path(a.state).expanduser()
    if a.once:
        try:
            for line in check(read, state, a.me, a.from_start):
                print(line, flush=True)
        except (OSError, ValueError, KeyError) as e:
            print(f"board_watch: {e}", file=sys.stderr, flush=True)
        return
    watch(read, None if a.poll else http_events(a.base), state, a.me, lambda line: print(line, flush=True),
          a.interval, a.from_start)


if __name__ == "__main__":
    main()
