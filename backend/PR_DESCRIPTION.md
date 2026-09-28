## Persist and query extracted video structure (graph store + vector search + `/ask`)

This is a really clever pipeline — the CLIP+OCR code extraction approach is genuinely novel, I haven't seen another video summarizer do that.

I noticed the knowledge graph and structured extraction (entities, steps, code snippets) were being generated per-request and returned as a one-off response. This PR extends things so extracted content is persisted and queryable, rather than discarded after each `/summarize` call.

### What's in this PR

**1. Persistent graph store (Neo4j)** — `graph_store.py`
Structured extraction (goal, steps, entities, concept-map triples, OCR'd code) is now written into Neo4j instead of only being returned in the response:

- `Video -[:HAS_STEP]-> Step`
- `Video -[:MENTIONS]-> Entity`, `Entity -[:RELATES]-> Entity` (from the existing concept-map triples)
- `Video -[:HAS_CODE]-> CodeSnippet`
- `Video -[:HAS_SEGMENT]-> Segment` (new — see below)

Concept maps and entities now accumulate across videos instead of vanishing after one response, enabling queries like "which videos cover X" or "show me every code snippet related to Y" (`videos_mentioning`, `related_entities`, `code_for_video`).

**2. Vector index over transcript + OCR'd code chunks** — `graph_store.py`
Added `store_segments()` / `semantic_search()`: transcript and OCR'd-code text are chunked (overlapping word windows) and embedded with `sentence-transformers` (`all-MiniLM-L6-v2` — already a project dependency via `visual_summary.py`, no new model download). Embeddings are stored as a property on `Segment` nodes in Neo4j; search does cosine-similarity ranking in Python over candidate vectors. No new vector-DB infra — if this needs to scale past a few thousand chunks, swap the ranking for Neo4j's native vector index (5.11+) without changing the call site.

**3. `/ask` endpoint — hybrid retrieval** — `qa_agent.py` (route already existed in `main.py`, logic upgraded)
- Relational questions ("which videos discuss recursion") → Cypher graph traversal
- Semantic questions ("what did they say about memoization") → vector search over transcript/code chunks
- Hybrid: when semantic search surfaces a chunk whose topic is also a known graph entity, related entities from the graph are attached as extra grounding for the LLM's answer
- Falls back to the existing structured-summary / entity-string-match paths if the vector index has nothing yet (e.g. a fresh deployment)

### Scope / risk
Additive only. Does **not** touch `video_processing.py`, `summary.py`, `visual_summary.py`, or the CLIP/OCR pipeline — those modules' outputs are just consumed by the new storage/indexing calls in `main.py`. Failures in `store_video_summary` / `store_segments` are caught and logged rather than breaking the `/summarize` or `/getcode` response.

### New dependencies
`neo4j`, `sentence-transformers`, `numpy` added to `requirements.txt`.

### Housekeeping (separate small commit)
`cookies.txt` (yt-dlp session cookies) isn't in `.gitignore` and appears to be tracked with a live, unexpired session. Added it to `.gitignore` here — **please also rotate that session and scrub it from git history** (`.gitignore` alone won't remove something already committed).
