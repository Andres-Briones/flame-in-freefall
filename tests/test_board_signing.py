import base64
import hashlib
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import pytest

from demo import board, board_id, ed25519

NOW = datetime(2026, 11, 14, 23, 2, tzinfo=timezone.utc)
SEED_A, SEED_B = bytes(range(32)), bytes(range(1, 33))
OPENSSL = {"public_key": "I1TfLwkeWahZzN4dIWrm0SMWiLoXtPUiNcMSXWfRyik=", "signed_at": "2026-11-14T23:01:52Z",
           "signature": "oAS+LLWNyNCMVDj/hMU5SjadG/prZFOAYqBIFjZatzHaVDcYPn/67toZCLId3hDdFjMcSni6WJQ5CsdDUYrVDg=="}
OPENSSL_BODY = "First signed post on the board: this line is the signed body."


@pytest.fixture(autouse=True)
def scratch_board(tmp_path, monkeypatch):
    monkeypatch.setattr(board, "DB_PATH", tmp_path / "board" / "board.db")
    monkeypatch.setattr(board, "_utcnow", lambda: NOW)


def signed(seed, author, target, body, when=NOW):
    return board_id.signed_args(seed, author, target, body, now=when)


def post(author, title, body, seed=None, **kw):
    sig = signed(seed, author, "new:" + title, body) if seed else {}
    return board.board_post(author=author, title=title, body=body, **sig, **kw)["data"]["thread"]


def messages(thread):
    return board.board_read(thread=thread)["data"]["thread"]["messages"]


# RFC 8032 section 7.1, tests 1, 2 and 3: secret key, public key, message, signature
RFC_VECTORS = [
    ("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
     "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
     "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
    ("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
     "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
     "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
    ("c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7",
     "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025", "af82",
     "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"),
]


@pytest.mark.parametrize("secret, public, message, signature", RFC_VECTORS)
def test_ed25519_matches_rfc_8032(secret, public, message, signature):
    seed, msg = bytes.fromhex(secret), bytes.fromhex(message)
    assert ed25519.public_key(seed).hex() == public
    assert ed25519.sign(seed, msg).hex() == signature
    assert ed25519.verify(bytes.fromhex(public), msg, bytes.fromhex(signature))
    assert not ed25519.verify(bytes.fromhex(public), msg + b"x", bytes.fromhex(signature))


@pytest.mark.parametrize("public, signature", [
    (b"", b""), (b"\x00" * 32, b"\x00" * 64), (b"\xff" * 32, b"\xff" * 64), ("text", "text"), (None, None),
    (bytes.fromhex(RFC_VECTORS[0][1]), bytes.fromhex(RFC_VECTORS[0][3])[:63]),
])
def test_verify_says_false_on_malformed_input(public, signature):
    assert ed25519.verify(public, b"m", signature) is False


def test_the_openssl_signature_of_thread_15_verifies_through_the_board():
    public = base64.b64decode(OPENSSL["public_key"])
    assert board.fingerprint(OPENSSL["public_key"]) == hashlib.sha256(public).hexdigest()[:16] == "5fa1a8c4eee7b3fd"
    for _ in range(14):
        post("Marta", "filler", "x")
    post("Claude (Andres)", "signing announced", "see the next reply")
    got = board.board_reply(thread=15, author=" Claude (Andres) ", body=OPENSSL_BODY + "\n", **OPENSSL)
    last = got["data"]["thread"]["messages"][-1]
    assert last["signature"] == "verified" and last["key"] == "5fa1a8c4eee7b3fd"
    assert board_id.verify("Claude (Andres)", "15", OPENSSL["signed_at"], OPENSSL_BODY, OPENSSL["public_key"],
                           OPENSSL["signature"])
    assert not board_id.verify("Claude (Andres)", "14", OPENSSL["signed_at"], OPENSSL_BODY, OPENSSL["public_key"],
                               OPENSSL["signature"])


def test_first_key_is_trusted_then_other_keys_and_unsigned_posts_are_marked():
    early = post("Claude (Marta)", "before keys", "unsigned, from before")
    first = post("Claude (Marta)", "hello", "signed", seed=SEED_A)
    assert first["messages"][0]["signature"] == "verified"
    key_a = board_id.fingerprint(ed25519.public_key(SEED_A))
    assert first["messages"][0]["key"] == key_a

    reply = signed(SEED_B, "claude (marta)", first["thread"], "impostor?")
    board.board_reply(thread=first["thread"], author="claude (marta)", body="impostor?", **reply)
    board.board_reply(thread=first["thread"], author="Claude (Marta)", body="no signature")
    board.board_reply(thread=first["thread"], author="Leo", body="never signs")
    marks = [(m.get("signature"), m.get("key")) for m in messages(first["thread"])]
    assert marks == [("verified", key_a), ("other_key", board_id.fingerprint(ed25519.public_key(SEED_B))),
                     ("unsigned", None), (None, None)]
    # older messages of a name that signs later carry no mark: they were written before the key was known
    assert "signature" not in messages(early["thread"])[0]

    data = board.board_read(status="all")["data"]
    assert [(i["author"], i["fingerprint"]) for i in data["identities"]] == [("Claude (Marta)", key_a)]
    listed = {t["title"]: t for t in data["threads"]}
    assert listed["hello"]["signature"] == "verified" and listed["hello"]["last_reply"].get("signature") is None
    assert data["threads"][0]["title"] == "hello" and listed["before keys"].get("signature") is None


def test_a_status_only_reply_signs_an_empty_body():
    t = post("Claude (Marta)", "t", "b", seed=SEED_A)
    got = board.board_reply(thread=t["thread"], author="Claude (Marta)", status="claimed",
                            **signed(SEED_A, "Claude (Marta)", t["thread"], ""))
    assert got["data"]["thread"]["messages"][-1]["signature"] == "verified"


@pytest.mark.parametrize("change, word", [
    ({"body": "tampered"}, "signed text must be"),
    ({"thread": 2}, "signed text must be"),
    ({"author": "Claude (Leo)"}, "signed text must be"),
    ({"when": NOW - timedelta(minutes=11)}, "minutes"),
    ({"when": NOW + timedelta(minutes=11)}, "minutes"),
    ({"signature": None}, "together"),
    ({"public_key": None, "signature": None}, "together"),
    ({"public_key": "not base64!"}, "public_key"),
    ({"signature": base64.b64encode(b"x" * 63).decode()}, "64 bytes"),
    ({"signed_at": "yesterday"}, "signed_at"),
])
def test_a_bad_signature_is_refused_and_nothing_is_stored(change, word):
    post("A", "one", "x")
    post("A", "two", "x")
    change = dict(change)
    args = {"thread": 1, "author": "Claude (Marta)", "body": "real body",
            **signed(SEED_A, "Claude (Marta)", 1, "real body", when=change.pop("when", NOW))}
    args.update(change)
    with pytest.raises(ValueError, match=word):
        board.board_reply(**args)
    assert board.board_read(status="all")["data"]["last_message"] == 2
    assert board.board_read()["data"]["identities"] == []


def test_a_signed_message_cannot_be_posted_twice():
    args = signed(SEED_A, "Claude (Marta)", "new:t", "b")
    board.board_post(author="Claude (Marta)", title="t", body="b", **args)
    with pytest.raises(ValueError, match="already"):
        board.board_post(author="Claude (Marta)", title="t", body="b", **args)


def test_a_board_from_before_signatures_gains_the_columns():
    board.DB_PATH.parent.mkdir(parents=True)
    with sqlite3.connect(board.DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE threads (id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, title TEXT NOT NULL,
                status TEXT NOT NULL, author TEXT NOT NULL, author_kind TEXT NOT NULL, to_name TEXT NOT NULL,
                created TEXT NOT NULL, updated TEXT NOT NULL, claimed_by TEXT);
            CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, thread_id INTEGER NOT NULL, author TEXT NOT NULL,
                author_kind TEXT NOT NULL, body TEXT NOT NULL, created TEXT NOT NULL);
            INSERT INTO threads VALUES (1, 'info', 'old', 'open', 'Claude (Marta)', 'ai', 'everyone',
                '2026-11-14T10:00:00Z', '2026-11-14T10:00:00Z', NULL);
            INSERT INTO messages VALUES (1, 1, 'Claude (Marta)', 'ai', 'old body', '2026-11-14T10:00:00Z');""")
    got = board.board_reply(thread=1, author="Claude (Marta)", body="now signed",
                            **signed(SEED_A, "Claude (Marta)", 1, "now signed"))["data"]["thread"]["messages"]
    assert [m.get("signature") for m in got] == [None, "verified"]


def test_the_client_reads_an_openssl_key_and_refuses_to_overwrite(tmp_path):
    openssl = pytest.importorskip("shutil").which("openssl")
    if not openssl:
        pytest.skip("openssl not installed")
    pem = tmp_path / "k.pem"
    subprocess.run([openssl, "genpkey", "-algorithm", "ed25519", "-out", str(pem)], check=True, capture_output=True)
    der = subprocess.run([openssl, "pkey", "-in", str(pem), "-pubout", "-outform", "DER"], check=True,
                         capture_output=True).stdout
    assert ed25519.public_key(board_id.read_key(pem)) == der[-32:]

    made = tmp_path / "new.pem"
    out = subprocess.run([sys.executable, board_id.__file__, "init", "--key", str(made)], capture_output=True, text=True)
    assert out.returncode == 0 and "fingerprint" in out.stdout and made.stat().st_mode & 0o777 == 0o600
    der = subprocess.run([openssl, "pkey", "-in", str(made), "-pubout", "-outform", "DER"], check=True,
                         capture_output=True).stdout
    assert base64.b64encode(der[-32:]).decode() in out.stdout
    again = subprocess.run([sys.executable, board_id.__file__, "init", "--key", str(made)], capture_output=True, text=True)
    assert again.returncode != 0 and "exists" in again.stderr


def test_the_client_signs_what_the_server_checks(monkeypatch):
    sent = []
    monkeypatch.setattr(board_id, "call", lambda base, fn, args: sent.append((fn, args)) or
                        {"data": board.FUNCTIONS[fn](**args)["data"]})
    monkeypatch.setattr(board_id, "read_key", lambda path: SEED_A)
    monkeypatch.setattr(board_id, "datetime", type("D", (), {"now": staticmethod(lambda tz: NOW)}))
    board_id.main(["post", "--key", "k", "--author", " Claude (Marta) ", "--title", " T ", "--body", " hello \n"])
    board_id.main(["reply", "--key", "k", "--author", "Claude (Marta)", "--thread", "1", "--status", "done",
                   "--body", ""])
    assert [m["signature"] for m in messages(1)] == ["verified", "verified"]
    assert sent[1][1]["status"] == "done" and "body" not in sent[1][1]


def test_the_signing_arguments_are_advertised():
    pytest.importorskip("fastapi")
    from fif import psi
    if not (psi.PROCESSED / "files.csv").exists():
        pytest.skip("processed tables not built")
    from fastapi.testclient import TestClient
    from demo import server
    client = TestClient(server.app)
    tools = {t["name"]: t for t in client.get("/api/tools").json()["board_tools"]}
    for name in ("board_post", "board_reply"):
        assert {"public_key", "signed_at", "signature"} <= set(tools[name]["input_schema"]["properties"])
    assert "fif-board-v1" in client.get("/llms.txt").text
    listed = client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).json()["result"]["tools"]
    assert "signature" in next(t for t in listed if t["name"] == "board_reply")["inputSchema"]["properties"]
    args = {"author": "Claude (Marta)", "title": "t", "body": "b", **signed(SEED_A, "Claude (Marta)", "new:t", "b")}
    made = client.post("/api/call/board_post", json=args).json()["data"]["thread"]["messages"][0]
    assert made["signature"] == "verified"
    bad = client.post("/api/call/board_post", json={**args, "body": "c"})
    assert bad.status_code == 400 and "signed text must be" in bad.json()["detail"]
