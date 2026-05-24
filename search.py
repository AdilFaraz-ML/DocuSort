import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Paths
FAISS_INDEX_PATH  = "faiss.index"
FILENAMES_MAP_PATH = "filenames_map.json"

# Load embedding model 
print("Loading embedding model (all-MiniLM-L6-v2)...")
_model = SentenceTransformer("all-MiniLM-L6-v2")

# Index Building

def build_index(documents: dict) -> tuple:
    """
    Embed all document texts and build a FAISS index.

    Args:
        documents: { filename: raw_text }

    Returns:
        (faiss.Index, list of filenames)
    """
    filenames = list(documents.keys())
    texts     = [documents[fn] for fn in filenames]

    print(f"\n Embedding {len(texts)} document(s)...")
    embeddings = _model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print(f" FAISS index built — {index.ntotal} vector(s) stored.")
    return index, filenames


def save_index(index, filenames: list) -> None:
    """Persist FAISS index and filename mapping to disk."""
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(FILENAMES_MAP_PATH, "w") as f:
        json.dump(filenames, f, indent=2)
    print(f" Index saved → {FAISS_INDEX_PATH}")


def load_index() -> tuple:
    """Load FAISS index and filename mapping from disk."""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            "FAISS index not found. Run the pipeline first: python main.py"
        )
    index     = faiss.read_index(FAISS_INDEX_PATH)
    with open(FILENAMES_MAP_PATH) as f:
        filenames = json.load(f)
    return index, filenames


# Search

def search_documents(query: str, output_data: dict, top_k: int = 5) -> list:
    """
    Semantic search over the FAISS index.

    Args:
        query:       Natural language query string
        output_data: Full output.json content
        top_k:       Number of results to return

    Returns:
        List of { filename, class, ...extracted_fields }
    """
    index, filenames = load_index()

    query_embedding = _model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx == -1 or idx >= len(filenames):
            continue
        filename = filenames[idx]
        doc_data = output_data.get(filename, {})
        results.append({
            "rank":     rank + 1,
            "filename": filename,
            "score":    float(round(distances[0][rank], 4)),
            "data":     doc_data,
        })

    return results
