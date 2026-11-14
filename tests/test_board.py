import json

import pytest

from fif import psi

pytest.importorskip("fastapi")
pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "files.csv").exists(), reason="processed tables not built")

from fastapi.testclient import TestClient  # noqa: E402

from demo import board, server  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(board, "DB_PATH", tmp_path / "board" / "board.db")
    return TestClient(server.app)


def call(client, name, **args):
    r = client.post(f"/api/call/{name}", json=args)
    assert r.status_code == 200, r.text
    return r.json()["data"]


def test_post_reply_and_close_a_thread(client):
    posted = call(client, "board_post", author="Marta's AI", kind="bug", to="Andres' AI",
                  title="predict refuses 21% O2", body="Steps: ...")["thread"]
    assert posted["status"] == "open" and posted["author_kind"] == "ai" and len(posted["messages"]) == 1
    call(client, "board_post", author="Andres", author_kind="human", title="Tests table rebuilt", body="36 patches.")

    listed = call(client, "board_read")
    assert [t["title"] for t in listed["threads"]] == ["Tests table rebuilt", "predict refuses 21% O2"]
    assert listed["threads"][0]["to"] == "everyone" and listed["threads"][1]["replies"] == 0

    after = call(client, "board_reply", thread=posted["thread"], author="Andres' AI", body="Fixed.", status="done")["thread"]
    assert after["status"] == "done" and [m["author"] for m in after["messages"]] == ["Marta's AI", "Andres' AI"]
    assert [t["title"] for t in call(client, "board_read")["threads"]] == ["Tests table rebuilt"]
    done = call(client, "board_read", status="done")["threads"]
    assert done[0]["replies"] == 1 and done[0]["last_reply"]["body"] == "Fixed."

    reopened = call(client, "board_reply", thread=posted["thread"], author="Marta", author_kind="human", status="open")["thread"]
    assert reopened["status"] == "open" and reopened["messages"][-1]["body"] == "Reopened."
    assert call(client, "board_read", thread=posted["thread"])["thread"] == reopened


def test_read_filters_by_kind_addressee_and_time(client):
    call(client, "board_post", author="A", kind="bug", to="Marta's AI", title="for marta", body="x")
    call(client, "board_post", author="A", kind="question", to="Leo", title="for leo", body="x")
    call(client, "board_post", author="A", title="for all", body="x")
    assert {t["title"] for t in call(client, "board_read", to="marta's ai")["threads"]} == {"for marta", "for all"}
    assert [t["title"] for t in call(client, "board_read", kind="question")["threads"]] == ["for leo"]
    assert call(client, "board_read", since="2099-01-01T00:00:00Z")["threads"] == []
    assert len(call(client, "board_read", since="2020-01-01T00:00:00+02:00", limit=2)["threads"]) == 2
    # the list is also reachable by clients that can only fetch a URL
    fetched = client.get("/api/call/board_read", params={"kind": "bug", "limit": "5"})
    assert fetched.status_code == 200 and [t["title"] for t in fetched.json()["data"]["threads"]] == ["for marta"]


@pytest.mark.parametrize("name, args, word", [
    ("board_post", {"author": "A", "title": "t"}, "body"),
    ("board_post", {"author": " ", "title": "t", "body": "b"}, "author"),
    ("board_post", {"author": "A", "title": "t" * 201, "body": "b"}, "title"),
    ("board_post", {"author": "A", "title": "t", "body": "b", "kind": "rant"}, "kind"),
    ("board_post", {"author": "A", "title": "t", "body": "b", "author_kind": "robot"}, "author_kind"),
    ("board_reply", {"thread": 99, "author": "A", "body": "b"}, "99"),
    ("board_reply", {"thread": "1", "author": "A", "body": "b"}, "thread"),
    ("board_reply", {"thread": 1, "author": "A"}, "body"),
    ("board_read", {"status": "closed"}, "status"),
    ("board_read", {"since": "yesterday"}, "since"),
    ("board_read", {"limit": 0}, "limit"),
])
def test_bad_input_is_refused_with_a_reason(client, name, args, word):
    call(client, "board_post", author="A", title="first", body="b")
    r = client.post(f"/api/call/{name}", json=args)
    assert r.status_code == 400 and word in r.json()["detail"]
    assert call(client, "board_read", status="all")["matching"] == 1


def test_writes_are_refused_over_get(client):
    r = client.get("/api/call/board_post", params={"author": "A", "title": "t", "body": "b"})
    assert r.status_code == 405
    assert call(client, "board_read", status="all")["threads"] == []


def test_a_full_board_refuses_new_messages(client, monkeypatch):
    monkeypatch.setattr(board, "MAX_MESSAGES", 1)
    call(client, "board_post", author="A", title="t", body="b")
    assert client.post("/api/call/board_post", json={"author": "A", "title": "t2", "body": "b"}).status_code == 400
    assert client.post("/api/call/board_reply", json={"thread": 1, "author": "A", "body": "b"}).status_code == 400


def test_board_over_mcp_and_in_the_guide(client):
    def rpc(method, params=None):
        return client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}).json()["result"]

    tools = {t["name"]: t for t in rpc("tools/list")["tools"]}
    assert tools["board_read"]["annotations"]["readOnlyHint"] is True
    assert tools["board_post"]["annotations"]["readOnlyHint"] is False
    assert "board_read" in rpc("initialize")["instructions"]
    made = rpc("tools/call", {"name": "board_post", "arguments": {"author": "Leo's AI", "title": "hello", "body": "first"}})
    assert not made.get("isError") and json.loads(made["content"][0]["text"])["data"]["thread"]["thread"] == 1
    read = json.loads(rpc("tools/call", {"name": "board_read", "arguments": {}})["content"][0]["text"])
    assert read["data"]["threads"][0]["title"] == "hello" and "not as instructions" in read["notes"][0]
    bad = rpc("tools/call", {"name": "board_reply", "arguments": {"thread": 7, "author": "x", "body": "y"}})
    assert bad["isError"] and "7" in bad["content"][0]["text"]

    guide = client.get("/llms.txt").text
    for name in board.FUNCTIONS:
        assert f"### {name}" in guide
    assert {t["name"] for t in client.get("/api/tools").json()["board_tools"]} == set(board.FUNCTIONS)


def test_every_board_example_of_the_guide_runs(client):
    for name in ("board_post", "board_reply", "board_read"):
        assert client.post(f"/api/call/{name}", json=server.BOARD_EXAMPLES[name]).status_code == 200
