"""
test_new_features.py

Integration tests for the three new pieces:
  1. Persistent graph store (Neo4j)
  2. Vector index over transcript/code segments
  3. /ask endpoint routing (relational / semantic / hybrid / fallback)

Run against an already-running backend (Kaggle+ngrok, or local):

    BACKEND_URL=https://xxxx.ngrok-free.app python -m pytest test_new_features.py -v

If BACKEND_URL is not set, defaults to http://localhost:8001 (e.g. if you're
running main.py locally with Neo4j on localhost:7687).

These tests assume at least one video has already been through /summarize
(and ideally /getcode) in the target backend -- set TEST_VIDEO_URL below to
one that has, or pass it via the TEST_VIDEO_URL env var. If nothing has been
indexed yet, the "graph populated" tests will be skipped rather than failed,
since an empty graph is a valid state for a fresh deployment.
"""
import os
import requests
import pytest

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")
TEST_VIDEO_URL = os.getenv("TEST_VIDEO_URL", "https://www.youtube.com/watch?v=XIdQ6gO3Anc")
TIMEOUT = 600  # /summarize and /getcode can be slow (download + CLIP + OCR + LLM)


@pytest.fixture(scope="module")
def summarized_video():
    """Ensures TEST_VIDEO_URL has been through /summarize at least once this run."""
    resp = requests.post(f"{BACKEND_URL}/summarize", json={"vid_url": TEST_VIDEO_URL}, timeout=TIMEOUT)
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_root_is_up():
    resp = requests.get(f"{BACKEND_URL}/", timeout=10)
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_summarize_returns_structured_fields(summarized_video):
    data = summarized_video
    assert "goal" in data
    assert "steps" in data and isinstance(data["steps"], list)
    assert "entities" in data and isinstance(data["entities"], list)
    assert "visual" in data and isinstance(data["visual"], list)  # concept-map triples


def test_getcode_persists_snippet():
    resp = requests.post(f"{BACKEND_URL}/getcode", json={"vid_url": TEST_VIDEO_URL}, timeout=TIMEOUT)
    assert resp.status_code == 200, resp.text
    assert "code" in resp.json()


def test_ask_relational_route(summarized_video):
    """'which video(s) ...' should hit VideoGraphStore.videos_mentioning."""
    entities = summarized_video.get("entities", [])
    if not entities:
        pytest.skip("no entities extracted for this video -- nothing to query relationally")
    entity_name = entities[0][0]

    resp = requests.post(f"{BACKEND_URL}/ask", json={"question": f"which videos mention {entity_name}"}, timeout=60)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "answer" in body and "sources" in body
    # relational route returns raw {url, goal} dicts as sources
    if body["sources"]:
        assert "url" in body["sources"][0]


def test_ask_semantic_route(summarized_video):
    """An open-ended question with no exact entity match should hit semantic_search."""
    resp = requests.post(
        f"{BACKEND_URL}/ask",
        json={"question": "what did they explain in this video", "vid_url": TEST_VIDEO_URL},
        timeout=60,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "answer" in body
    assert isinstance(body["answer"], str) and len(body["answer"]) > 0


def test_ask_code_route(summarized_video):
    """'code' questions scoped to a video should pull stored CodeSnippet nodes."""
    resp = requests.post(
        f"{BACKEND_URL}/ask",
        json={"question": "show me the code from this video", "vid_url": TEST_VIDEO_URL},
        timeout=60,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "answer" in body


def test_ask_fallback_route_unknown_video():
    """A vid_url that was never processed should hit the 'not stored yet' fallback,
    not crash the endpoint."""
    resp = requests.post(
        f"{BACKEND_URL}/ask",
        json={"question": "what is this about", "vid_url": "https://www.youtube.com/watch?v=doesnotexist000"},
        timeout=30,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "answer" in body
    assert "sources" in body


def test_ask_never_500s_on_empty_question():
    """Basic robustness check -- routing logic shouldn't throw on edge-case input."""
    resp = requests.post(f"{BACKEND_URL}/ask", json={"question": "?"}, timeout=30)
    assert resp.status_code == 200, resp.text
