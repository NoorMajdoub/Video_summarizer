"""
graph_store.py
Persists per-video extraction output (entity/relation triples, structured
summary, extracted code) into Neo4j, and provides simple read queries for
the /ask endpoint.

This does NOT touch video_processing.py, summary.py, or visual_summary.py.
It only consumes what those modules already return.

Vector search
--------------
Segment nodes (transcript or OCR'd-code chunks) store a sentence embedding
as a plain list-of-floats property (`embedding`). There's no dependency on
a separate vector DB / FAISS index: at query time we pull candidate
Segment vectors out of Neo4j and do the cosine-similarity ranking in
Python with numpy. This is intentionally simple -- it's fine at the scale
a Kaggle-hosted demo backend runs at, and it means `/ask` gets semantic
search without adding new infra beyond Neo4j (which is already required
for the graph). If this ever needs to scale past a few thousand chunks,
swap `semantic_search`'s Cypher for Neo4j's native vector index
(`db.index.vector.queryNodes`, Neo4j 5.11+) -- the call site doesn't need
to change.
"""
import os
import numpy as np
from neo4j import GraphDatabase

_EMBEDDER = None


def _get_embedder():
    """Lazily load the sentence embedder (reuses the same model already
    used in visual_summary.py, so no new model weights to download)."""
    global _EMBEDDER
    if _EMBEDDER is None:
        from sentence_transformers import SentenceTransformer
        _EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
    return _EMBEDDER


def _chunk_text(text, max_words=120, overlap=20):
    """Splits text into overlapping word-window chunks for embedding.
    Overlap keeps a concept from being split awkwardly across chunk
    boundaries."""
    if not text or not text.strip():
        return []
    words = text.split()
    if len(words) <= max_words:
        return [text.strip()]

    chunks = []
    step = max(max_words - overlap, 1)
    for start in range(0, len(words), step):
        piece = " ".join(words[start:start + max_words]).strip()
        if piece:
            chunks.append(piece)
        if start + max_words >= len(words):
            break
    return chunks


class VideoGraphStore:
    def __init__(self, uri=None, user=None, password=None):
        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = user or os.getenv("NEO4J_USER", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # ---------- writes ----------

    def store_video_summary(self, vid_url, parsed, triples, code=None):
        """
        Args:
            vid_url: the youtube url, used as the Video node's unique key
            parsed: dict from prompt_2_json() -> goal, global_understanding,
                    steps (list[str]), entities (list[[name, desc]])
            triples: list of [entity1, verb, entity2] from get_graph_nlp()
            code: optional cleaned code string from code_extraction_pipeline()
        """
        with self.driver.session() as session:
            session.execute_write(self._write_video_meta, vid_url, parsed)
            for e1, verb, e2 in triples:
                session.execute_write(self._write_triple, vid_url, e1, verb, e2)
            if code:
                session.execute_write(self._write_code, vid_url, code)

    @staticmethod
    def _write_video_meta(tx, vid_url, parsed):
        tx.run(
            """
            MERGE (v:Video {url: $url})
            SET v.goal = $goal,
                v.global_understanding = $global_understanding
            """,
            url=vid_url,
            goal=parsed.get("goal", ""),
            global_understanding=parsed.get("global_understanding", ""),
        )
        for step in parsed.get("steps", []):
            tx.run(
                """
                MATCH (v:Video {url: $url})
                CREATE (s:Step {text: $step})
                MERGE (v)-[:HAS_STEP]->(s)
                """,
                url=vid_url, step=step,
            )
        for name, desc in parsed.get("entities", []):
            tx.run(
                """
                MATCH (v:Video {url: $url})
                MERGE (e:Entity {name: $name})
                SET e.description = $desc
                MERGE (v)-[:MENTIONS]->(e)
                """,
                url=vid_url, name=name, desc=desc,
            )

    @staticmethod
    def _write_triple(tx, vid_url, e1, verb, e2):
        tx.run(
            """
            MATCH (v:Video {url: $url})
            MERGE (a:Entity {name: $e1})
            MERGE (b:Entity {name: $e2})
            MERGE (a)-[r:RELATES {verb: $verb}]->(b)
            MERGE (v)-[:MENTIONS]->(a)
            MERGE (v)-[:MENTIONS]->(b)
            """,
            url=vid_url, e1=e1, e2=e2, verb=verb,
        )

    @staticmethod
    def _write_code(tx, vid_url, code):
        tx.run(
            """
            MATCH (v:Video {url: $url})
            CREATE (c:CodeSnippet {content: $code})
            MERGE (v)-[:HAS_CODE]->(c)
            """,
            url=vid_url, code=code,
        )

    # ---------- vector index (transcript + OCR code chunks) ----------

    def store_segments(self, vid_url, transcript_text=None, code_text=None):
        """
        Chunks and embeds transcript/code text and stores each chunk as a
        Segment node linked to the Video, so /ask can do semantic search
        over it later. Safe to call multiple times for the same video
        (e.g. once from /summarize with the transcript, once from
        /getcode with the extracted code) -- chunks just accumulate.

        Args:
            vid_url: the youtube url, matches the Video node written by
                     store_video_summary()
            transcript_text: raw transcript string, or None
            code_text: cleaned OCR'd code string, or None
        """
        embedder = _get_embedder()
        segments = []
        for text, kind in ((transcript_text, "transcript"), (code_text, "code")):
            for chunk in _chunk_text(text):
                segments.append((chunk, kind))

        if not segments:
            return

        vectors = embedder.encode([c for c, _ in segments])
        with self.driver.session() as session:
            session.execute_write(self._write_video_stub, vid_url)
            for (chunk, kind), vector in zip(segments, vectors):
                session.execute_write(
                    self._write_segment, vid_url, chunk, kind, vector.tolist()
                )

    @staticmethod
    def _write_video_stub(tx, vid_url):
        # MERGE so this works even if called before store_video_summary()
        # (e.g. /getcode can run before /summarize has stored the video).
        tx.run("MERGE (v:Video {url: $url})", url=vid_url)

    @staticmethod
    def _write_segment(tx, vid_url, text, kind, embedding):
        tx.run(
            """
            MATCH (v:Video {url: $url})
            CREATE (s:Segment {text: $text, kind: $kind, embedding: $embedding})
            MERGE (v)-[:HAS_SEGMENT]->(s)
            """,
            url=vid_url, text=text, kind=kind, embedding=embedding,
        )

    def semantic_search(self, query, top_k=5, kind=None, vid_url=None):
        """
        Embeds `query` and ranks stored Segment chunks by cosine
        similarity, computed in Python over vectors pulled from Neo4j.

        Args:
            query: natural-language question/text to search for
            top_k: how many chunks to return
            kind: optional filter, "transcript" or "code"
            vid_url: optional filter, scope search to one video
        Returns:
            list of {"vid_url", "text", "kind", "score"}, best first
        """
        embedder = _get_embedder()
        query_vec = embedder.encode([query])[0]

        filters = []
        params = {}
        if kind:
            filters.append("s.kind = $kind")
            params["kind"] = kind
        if vid_url:
            filters.append("v.url = $vid_url")
            params["vid_url"] = vid_url
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        with self.driver.session() as session:
            result = session.run(
                f"""
                MATCH (v:Video)-[:HAS_SEGMENT]->(s:Segment)
                {where_clause}
                RETURN v.url AS vid_url, s.text AS text, s.kind AS kind,
                       s.embedding AS embedding
                """,
                **params,
            )
            rows = [dict(r) for r in result]

        if not rows:
            return []

        matrix = np.array([r["embedding"] for r in rows], dtype=float)
        norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_vec)
        norms[norms == 0] = 1e-8  # avoid divide-by-zero on empty embeddings
        scores = (matrix @ query_vec) / norms

        ranked = sorted(
            (
                {"vid_url": r["vid_url"], "text": r["text"], "kind": r["kind"], "score": float(score)}
                for r, score in zip(rows, scores)
            ),
            key=lambda r: r["score"],
            reverse=True,
        )
        return ranked[:top_k]

    # ---------- reads (used by qa_agent.py) ----------

    def videos_mentioning(self, entity_name):
        """Relational query: which videos mention/discuss this entity."""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (v:Video)-[:MENTIONS]->(e:Entity)
                WHERE toLower(e.name) CONTAINS toLower($name)
                RETURN DISTINCT v.url AS url, v.goal AS goal
                """,
                name=entity_name,
            )
            return [dict(r) for r in result]

    def related_entities(self, entity_name, hops=1):
        """Graph traversal: entities connected to a given entity, up to N hops."""
        with self.driver.session() as session:
            result = session.run(
                f"""
                MATCH (a:Entity)-[:RELATES*1..{hops}]-(b:Entity)
                WHERE toLower(a.name) CONTAINS toLower($name)
                RETURN DISTINCT b.name AS related
                LIMIT 25
                """,
                name=entity_name,
            )
            return [r["related"] for r in result]

    def code_for_video(self, vid_url):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (v:Video {url: $url})-[:HAS_CODE]->(c:CodeSnippet)
                RETURN c.content AS content
                """,
                url=vid_url,
            )
            return [r["content"] for r in result]

    def video_summary(self, vid_url):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (v:Video {url: $url})
                OPTIONAL MATCH (v)-[:HAS_STEP]->(s:Step)
                OPTIONAL MATCH (v)-[:MENTIONS]->(e:Entity)
                RETURN v.goal AS goal, v.global_understanding AS overview,
                       collect(DISTINCT s.text) AS steps,
                       collect(DISTINCT e.name) AS entities
                """,
                url=vid_url,
            )
            record = result.single()
            return dict(record) if record else None