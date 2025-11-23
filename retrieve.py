# retrieve.py
import json, os
import chromadb
from sentence_transformers import SentenceTransformer

EMB_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def get_collection():
    client = chromadb.PersistentClient(path="data/chroma_store")
    if "snippets" not in [c.name for c in client.list_collections()]:
        client.create_collection("snippets")
    return client.get_collection("snippets")

def ensure_index():
    coll = get_collection()
    count = coll.count()
    if count > 0:
        return coll

    # Build index from snippets.jsonl
    model = SentenceTransformer(EMB_MODEL_NAME)
    items, ids = [], []
    with open("data/snippets.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            items.append(obj["text"])
            ids.append(obj["id"])

    coll.add(ids=ids, documents=items)
    return coll

def query_snippets(jd_text: str, top_k: int = 20):
    model = SentenceTransformer(EMB_MODEL_NAME)
    emb = model.encode([jd_text], normalize_embeddings=True)[0]  # not stored; used for re-ranking
    coll = ensure_index()
    # Chroma’s semantic search
    res = coll.query(query_texts=[jd_text], n_results=top_k)
    hits = res["documents"][0]
    return hits
