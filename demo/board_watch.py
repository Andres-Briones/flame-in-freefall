"""Watch the team board: print one line for each new message that somebody else wrote, and nothing while the board
is quiet. Meant to run beside an AI assistant's session (each line wakes the assistant), or from a timer with --once.

    python demo/board_watch.py --me "Claude (Andres)" --state ~/.board-watch.json

The state file keeps the id of the last message seen, so a restart neither repeats nor misses messages. The first
run with a new state file starts from the present; --from-start prints the whole board instead. Standard library
only, so it runs without the project's environment.
"""
import argparse
import json
import sys
import time
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
                body = " ".join(m["body"].split())
                lines.append(f"thread {t['thread']} [{t['kind']}, {t['status']}, for {t['to']}] \"{t['title']}\" "
                             f"message {m['id']} from {m['author']}: {body[:300]}")
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps({"last_message": cursor}))
    return lines


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--me", required=True, help="your signature on the board; your own messages are not reported")
    p.add_argument("--state", required=True, help="file that remembers the last message seen")
    p.add_argument("--base", default=DEFAULT_BASE)
    p.add_argument("--interval", type=float, default=45, help="seconds between checks")
    p.add_argument("--once", action="store_true", help="check once and exit")
    p.add_argument("--from-start", action="store_true", help="with a new state file, report the whole board")
    a = p.parse_args()
    read = http_read(a.base)
    while True:
        try:
            for line in check(read, Path(a.state).expanduser(), a.me, a.from_start):
                print(line, flush=True)
        except (OSError, ValueError, KeyError) as e:
            # a server restart during a deploy must not end the watch
            print(f"board_watch: {e}", file=sys.stderr, flush=True)
        if a.once:
            return
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
