"""
qa_agent.py
Answers natural-language questions over the persisted video graph.

Routing:
  1. "which/what video(s) ..." -> relational graph traversal
     (VideoGraphStore.videos_mentioning)
  2. "... code ..." scoped to a video -> stored CodeSnippet lookup
  3. everything else -> semantic search over embedded transcript/OCR-code
     Segment chunks (VideoGraphStore.semantic_search), optionally combined
     with a relational entity lookup when the retrieved chunks mention a
     named entity that's also in the graph -- that's the "hybrid" case:
     vector search finds *where* the answer likely lives, the graph
     supplies *what else* connects to it.
  4. if semantic search finds nothing (empty graph, brand-new deployment)
     -> fall back to the old string-matching entity lookup so /ask still
     returns something useful.
"""
import re
from llm_call import call_llm
from graph_store import VideoGraphStore


def _extract_entity(question):
    """
    Very small heuristic extractor: pulls a likely topic/entity out of
    the question. Good enough as a first pass -- swap for spaCy NER
    (already a dependency, used in visual_summary.py) if this is too weak.
    """
    match = re.search(
        r"(?:about|on|regarding|mention(?:s|ing)?)\s+([A-Za-z0-9_\- ]+)",
        question,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip(" ?.")
    # fallback: last capitalized-looking token or noun-ish word
    words = [w.strip("?.,") for w in question.split()]
    return words[-1] if words else question


def answer_question(question, store: VideoGraphStore, vid_url: str = None):
    """
    Args:
        question: user's natural-language question
        store: an open VideoGraphStore
        vid_url: optional -- if the question is scoped to one video already
                 loaded in the graph (e.g. asked right after /summarize)
    Returns:
        dict with 'answer' and 'sources' (raw data used to ground it)
    """
    q_lower = question.lower()

    # Route 1: "which videos ... about X" -> relational graph query
    if any(kw in q_lower for kw in ["which video", "what video", "videos about", "videos mention"]):
        entity = _extract_entity(question)
        matches = store.videos_mentioning(entity)
        if not matches:
            return {"answer": f"No stored videos currently mention '{entity}'.", "sources": []}
        listing = "\n".join(f"- {m['url']} ({m['goal']})" for m in matches)
        return {"answer": f"Videos mentioning '{entity}':\n{listing}", "sources": matches}

    # Route 2: "code" questions -> pull stored code for a specific video
    if "code" in q_lower and vid_url:
        snippets = store.code_for_video(vid_url)
        if not snippets:
            return {"answer": "No code was extracted/stored for this video.", "sources": []}
        return {"answer": "\n\n---\n\n".join(snippets), "sources": snippets}

    # Route 3: semantic search over embedded transcript/code chunks,
    # optionally scoped to one video. This is the main "what did they say
    # about X" path -- it doesn't require the question to name an entity
    # verbatim, unlike the old string-matching fallback.
    chunks = store.semantic_search(question, top_k=5, vid_url=vid_url)

    if chunks:
        # Hybrid step: pull the topic out of the question and see if it's
        # also a known graph entity. If so, attach related entities/videos
        # as extra grounding alongside the retrieved text chunks.
        entity = _extract_entity(question)
        related = store.related_entities(entity) if not vid_url else []

        context = "\n\n---\n\n".join(
            f"[{c['kind']} chunk from {c['vid_url']}]\n{c['text']}" for c in chunks
        )
        graph_context = f"\n\nAlso related in the graph: {', '.join(related)}" if related else ""

        prompt = (
            "Using ONLY the context below (retrieved transcript/code chunks, "
            "plus any related graph entities), answer the question. If the "
            "context doesn't contain the answer, say so.\n\n"
            f"Context:\n{context}{graph_context}\n\n"
            f"Question: {question}\n\nAnswer concisely:"
        )
        answer = call_llm(prompt)
        return {"answer": answer, "sources": chunks + ([{"related_entities": related}] if related else [])}

    # Route 4 (fallback): semantic index is empty (e.g. nothing stored
    # yet, or embeddings weren't generated for older videos) -> fall back
    # to structured summary for a scoped video, else cross-video entity
    # string-matching, same as before.
    if vid_url:
        summary = store.video_summary(vid_url)
        if summary is None:
            return {"answer": "This video hasn't been processed/stored yet.", "sources": []}
        context = (
            f"Goal: {summary['goal']}\n"
            f"Overview: {summary['overview']}\n"
            f"Steps: {summary['steps']}\n"
            f"Entities: {summary['entities']}"
        )
        prompt = (
            f"Using ONLY the following stored context about a video, answer the question.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer concisely:"
        )
        answer = call_llm(prompt)
        return {"answer": answer, "sources": [summary]}

    entity = _extract_entity(question)
    related = store.related_entities(entity)
    if related:
        return {
            "answer": f"'{entity}' is connected to: {', '.join(related)} across stored videos.",
            "sources": related,
        }
    return {"answer": "I couldn't find anything relevant in the stored graph yet.", "sources": []}