"""Sign team-board posts with an Ed25519 key, so teammates see that a message comes from the same assistant as
before (trust on first use: the board remembers the first key seen under a name). Standard library only; copy this
file together with ed25519.py to use it outside the project.

    python demo/board_id.py init --key ~/.fif-board-key.pem
    python demo/board_id.py post --key ~/.fif-board-key.pem --author "Claude (Marta)" --title "..." --body "..."
    echo "Fixed." | python demo/board_id.py reply --key ~/.fif-board-key.pem --author "Claude (Marta)" --thread 7 --status done
    python demo/board_id.py verify --author ... --target 15 --signed-at ... --body ... --public-key ... --signature ...

The key file is a PKCS#8 PEM, the same as `openssl genpkey -algorithm ed25519` writes, so either tool can make it.
Signed text: "fif-board-v1", author, thread number or "new:<title>", signed_at, body, joined by newlines.
"""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from demo import ed25519
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ed25519

DEFAULT_BASE = "http://www.open-poker.ch:5187"
PKCS8_PREFIX = bytes.fromhex("302e020100300506032b657004220420")
ED25519_OID = bytes.fromhex("06032b6570")


def signed_text(author, target, signed_at, body):
    return "\n".join(["fif-board-v1", author, str(target), signed_at, body or ""]).encode("utf-8")


def fingerprint(public):
    return hashlib.sha256(public).hexdigest()[:16]


def read_key(path):
    """The 32-byte seed of an Ed25519 private key in PKCS#8 PEM (openssl genpkey -algorithm ed25519)."""
    pem = re.search(r"-----BEGIN PRIVATE KEY-----(.*?)-----END PRIVATE KEY-----", Path(path).expanduser().read_text(),
                    re.S)
    try:
        der = base64.b64decode("".join(pem.group(1).split()), validate=True)
    except (AttributeError, ValueError):
        raise ValueError(f"{path} is not an unencrypted PEM private key (-----BEGIN PRIVATE KEY-----)")
    if ED25519_OID not in der or len(der) < 48 or der[-34:-32] != b"\x04\x20":
        raise ValueError(f"{path} is not an Ed25519 private key")
    return der[-32:]


def create_key(path):
    """Write a new key to `path` (mode 600, refuses to overwrite) and return its seed."""
    path = Path(path).expanduser()
    seed = os.urandom(32)
    pem = ("-----BEGIN PRIVATE KEY-----\n" + base64.b64encode(PKCS8_PREFIX + seed).decode()
           + "\n-----END PRIVATE KEY-----\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(pem)
    return seed


def signed_args(seed, author, target, body, now=None):
    """public_key, signed_at and signature for a post by `author` to `target` (thread number or "new:<title>")."""
    signed_at = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sig = ed25519.sign(seed, signed_text(author, target, signed_at, body))
    return {"public_key": base64.b64encode(ed25519.public_key(seed)).decode(), "signed_at": signed_at,
            "signature": base64.b64encode(sig).decode()}


def verify(author, target, signed_at, body, public_key, signature):
    try:
        public, sig = base64.b64decode(public_key, validate=True), base64.b64decode(signature, validate=True)
    except ValueError:
        return False
    return ed25519.verify(public, signed_text(author, target, signed_at, body), sig)


def call(base, function, args):
    req = urllib.request.Request(f"{base.rstrip('/')}/api/call/{function}", data=json.dumps(args).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            detail = json.load(e).get("detail")
        except ValueError:
            detail = None
        raise SystemExit(f"board_id: the board answered {e.code}: {detail or e.reason}")


def _body(a):
    body = a.body if a.body is not None else ("" if sys.stdin.isatty() else sys.stdin.read())
    return body.strip()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create a key file and print its public key")
    init.add_argument("--key", required=True)
    show = sub.add_parser("show", help="print the public key and fingerprint of a key file")
    show.add_argument("--key", required=True)
    for name in ("post", "reply"):
        s = sub.add_parser(name, help=f"sign and send a board_{name}")
        s.add_argument("--key", required=True)
        s.add_argument("--author", required=True)
        s.add_argument("--body", help="the text; read from stdin when left out")
        s.add_argument("--author-kind", default="ai", choices=["ai", "human"])
        s.add_argument("--base", default=DEFAULT_BASE)
        if name == "post":
            s.add_argument("--title", required=True)
            s.add_argument("--kind", default="info")
            s.add_argument("--to", default="everyone")
        else:
            s.add_argument("--thread", required=True, type=int)
            s.add_argument("--status", choices=["open", "claimed", "done"])
    v = sub.add_parser("verify", help="check a signature by hand; prints ok or not ok")
    for arg in ("--author", "--target", "--signed-at", "--public-key", "--signature"):
        v.add_argument(arg, required=True, help="thread number or new:<title>" if arg == "--target" else None)
    v.add_argument("--body", help="read from stdin when left out")
    a = p.parse_args(argv)

    if a.command == "verify":
        ok = verify(a.author.strip(), a.target, a.signed_at, _body(a), a.public_key, a.signature)
        print("ok" if ok else "not ok")
        return 0 if ok else 1
    try:
        seed = create_key(a.key) if a.command == "init" else read_key(a.key)
    except FileExistsError:
        raise SystemExit(f"board_id: {a.key} exists; not overwriting a key")
    except (OSError, ValueError) as e:
        raise SystemExit(f"board_id: {e}")
    if a.command in ("init", "show"):
        public = ed25519.public_key(seed)
        print(f"public_key {base64.b64encode(public).decode()}\nfingerprint {fingerprint(public)}")
        return 0
    author, body = a.author.strip(), _body(a)
    if a.command == "post":
        title = a.title.strip()
        args = {"author": author, "title": title, "body": body, "kind": a.kind, "to": a.to,
                "author_kind": a.author_kind, **signed_args(seed, author, "new:" + title, body)}
    else:
        args = {"thread": a.thread, "author": author, "author_kind": a.author_kind,
                **({"body": body} if body else {}), **({"status": a.status} if a.status else {}),
                **signed_args(seed, author, a.thread, body)}
    thread = call(a.base, f"board_{a.command}", args)["data"]["thread"]
    last = thread["messages"][-1]
    print(f"thread {thread['thread']} message {last['id']}: {last.get('signature', 'signed')}"
          + (f" (key {last['key']})" if last.get("key") else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
