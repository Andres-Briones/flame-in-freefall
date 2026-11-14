"""The live board feed. The TestClient waits for a response to finish, so the never-ending stream is read by driving
the endpoint's generator directly; status codes and headers that do not need the body go through the client."""
import asyncio
import json
import urllib.error

import pytest

from fif import psi

pytest.importorskip("fastapi")
pytestmark = pytest.mark.skipif(not (psi.PROCESSED / "files.csv").exists(), reason="processed tables not built")

from fastapi.testclient import TestClient  # noqa: E402
from starlette.requests import Request  # noqa: E402

from demo import board, board_watch, server  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(board, "DB_PATH", tmp_path / "board" / "board.db")
    return TestClient(server.app)


def request(query="", headers=()):
    return Request({"type": "http", "method": "GET", "path": "/api/board/events", "query_string": query.encode(),
                    "headers": [(k.lower().encode(), v.encode()) for k, v in headers]})


def take(query="", headers=(), n=1, between=None):
    """The first `n` chunks of the stream opened with this query and headers; `between` runs after it is opened."""
    async def run():
        response = await server.board_events(request(query, headers))
        assert response.media_type == "text/event-stream" and response.headers["x-accel-buffering"] == "no"
        stream = response.body_iterator
        if between:
            between()
        try:
            return [await asyncio.wait_for(anext(stream), 5) for _ in range(n)]
        finally:
            await stream.aclose()
    return asyncio.run(run())


def parse(chunk):
    fields = dict(line.split(": ", 1) for line in chunk.strip().split("\n"))
    return int(fields["id"]), json.loads(fields["data"])


def test_the_stream_starts_from_the_present_and_carries_no_body(client):
    board.board_post(author="A", title="old", body="before connecting")
    chunks = take(between=lambda: board.board_reply(thread=1, author="Marta", body="secret text", status="claimed"))
    msg_id, event = parse(chunks[0])
    assert msg_id == 2 and event == {"thread": 1, "id": 2, "author": "Marta", "author_kind": "ai", "to": "everyone",
                                     "kind": "info", "title": "old", "created": event["created"]}
    assert "secret text" not in chunks[0] and server._event_streams == 0


def test_the_stream_resumes_after_a_message_or_the_last_event_id(client):
    for i in range(3):
        board.board_post(author="A", title=f"t{i}", body="b")
    assert [parse(c)[0] for c in take("after_message=0", n=3)] == [1, 2, 3]
    assert [parse(c)[0] for c in take("after_message=0", headers=[("Last-Event-ID", "2")])] == [3]


def test_the_stream_keeps_quiet_connections_alive(client, monkeypatch):
    async def run():
        stream = server.board_event_stream(0, poll_s=0.01, keepalive_s=0.05)
        try:
            return await asyncio.wait_for(anext(stream), 5)
        finally:
            await stream.aclose()
    assert asyncio.run(run()) == ": keepalive\n\n"


def test_the_stream_refuses_bad_starts_and_too_many_listeners(client, monkeypatch):
    assert client.get("/api/board/events", params={"after_message": "x"}).status_code == 400
    assert client.get("/api/board/events", headers={"Last-Event-ID": "-3"}).status_code == 400
    monkeypatch.setattr(server, "_event_streams", server.MAX_EVENT_STREAMS)
    assert client.get("/api/board/events").status_code == 503


def test_the_feed_is_in_the_guide(client):
    assert "/api/board/events" in client.get("/llms.txt").text
    assert "/api/board/events" in client.get("/api/tools").json()["board_events"]


def test_the_watcher_follows_the_stream_and_reads_bodies(client, tmp_path):
    def read(**args):
        r = client.post("/api/call/board_read", json=args)
        return r.json()["data"]

    def events(after):
        board.board_reply(thread=1, author="Claude (Andres)", body="mine")
        board.board_reply(thread=1, author="Marta", body="hello\nthere")
        yield from board.events_after(after)

    board.board_post(author="A", title="t", body="b")
    state, lines = tmp_path / "w.json", []
    board_watch.check(read, state, "Claude (Andres)")
    board_watch.follow(events, read, state, "Claude (Andres)", lines.append)
    assert lines == ['thread 1 [info, open, for everyone] "t" message 3 from Marta: hello there']
    assert json.loads(state.read_text())["last_message"] == 3


def test_the_watcher_polls_when_the_server_has_no_stream(client, tmp_path):
    def read(**args):
        return client.post("/api/call/board_read", json=args).json()["data"]

    opened, lines, sleeps = [], [], []

    def events(after):
        opened.append(after)
        raise board_watch.NoStream()
        yield

    def sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) == 1:
            board.board_post(author="Marta", title="polled", body="found by polling")
        else:
            raise StopIteration

    board.board_post(author="A", title="t", body="b")
    with pytest.raises(StopIteration):
        board_watch.watch(read, events, tmp_path / "w.json", "Claude (Andres)", lines.append, 45, sleep=sleep)
    assert opened == [1] and sleeps == [45, 45]
    assert lines == ['thread 2 [info, open, for everyone] "polled" message 2 from Marta: found by polling']


def test_http_events_turns_a_404_into_no_stream(monkeypatch):
    def refuse(*args, **kwargs):
        raise urllib.error.HTTPError("http://x/api/board/events", 404, "Not Found", {}, None)
    monkeypatch.setattr(board_watch.urllib.request, "urlopen", refuse)
    with pytest.raises(board_watch.NoStream):
        next(board_watch.http_events("http://x")(0))
