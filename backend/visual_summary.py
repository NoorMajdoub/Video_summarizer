"""
visual_summary.py
Generates entity-relation knowledge graph data from a video transcript using spaCy and text embeddings
"""
 
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy

def get_graph_nlp(transcript):
    """
    Extracts simple knowledge graph triples from the text using spaCy , computes semantic similarity between
    entities using the embedding of the sentence
    """
    nlp = spacy.load("en_core_web_sm")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")  
    doc = nlp(transcript[:5000])
    
    # we extract unique entities
    entities = list(set(
        e.text.strip() for e in doc.ents
        if e.label_ in ["PERSON", "ORG", "PRODUCT", "GPE", "WORK_OF_ART"]
        and len(e.text.strip()) > 2
        and not e.text.isnumeric()
    ))
    
    if len(entities) < 2:
        return []
   
    entities = entities[:10] 
    # embed all entities
    embeddings = embedder.encode(entities)
    sim_matrix = cosine_similarity(embeddings)
    
    triples = []
    seen = set()
    weak_verbs = {"go", "want", "do", "get", "have", "be", "say", "make", "use"}

    for sent in doc.sents:
        sent_ents = [e.text.strip() for e in sent.ents if e.text.strip() in entities]
        if len(sent_ents) < 2:
            continue
        
        e1, e2 = sent_ents[0], sent_ents[1]
        if e1 == e2 or (e1, e2) in seen:
            continue
        
        # get similarity score between these two entities
        i, j = entities.index(e1), entities.index(e2)
        score = sim_matrix[i][j]
        
        # finds the verb needed to connect the entities
        verb = next(
            (t.lemma_ for t in sent if t.pos_ == "VERB" and t.lemma_ not in weak_verbs),
            "relates to" if score > 0.4 else "connects to"
        )
        
        seen.add((e1, e2))
        triples.append([e1, verb, e2])
        
        if len(triples) >= 6:
            break
    
    return triples
 
