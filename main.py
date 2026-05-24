import os
import sys
import json

from extractor      import load_documents
from classifier     import classify_document
from field_extractor import extract_fields
from search         import build_index, save_index, search_documents

DOCUMENTS_FOLDER = "documents"
OUTPUT_JSON_PATH = "output.json"


# Pipeline

def run_pipeline():
    """
    Full pipeline:
        Load documents → Classify → Extract fields → Save output.json → Build FAISS index
    """
    print("=" * 55)
    print("  DocuSort — Document Classification Pipeline")
    print("=" * 55)

    # Step 1: Load documents
    documents = load_documents(DOCUMENTS_FOLDER)
    if not documents:
        print("\n[ERROR] No documents to process. Add files to the 'documents/' folder.")
        return

    # Step 2: Classify + Extract
    output = {}
    print(f"\n Processing {len(documents)} document(s)...\n")

    for filename, text in documents.items():
        doc_class = classify_document(text)
        fields    = extract_fields(doc_class, text)

        output[filename] = {"class": doc_class, **fields}

        print(f"  {filename}")
        print(f"     Class  : {doc_class}")
        for key, val in fields.items():
            print(f"     {key:<20}: {val}")
        print()

    # Step 3: Save output.json
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f" output.json saved → {OUTPUT_JSON_PATH}")

    # Step 4: Build and save FAISS index
    print()
    index, filenames = build_index(documents)
    save_index(index, filenames)

    print("\n" + "=" * 55)
    print("  Pipeline complete.")
    print(f"  → {len(output)} document(s) processed")
    print(f"  → output.json saved")
    print(f"  → FAISS index ready")
    print("=" * 55)
    print("\nTo search: python main.py search")


# Search Mode

def run_search(direct_query: str = None):
    """
    Interactive or direct semantic search over processed documents.
    Returns the structured JSON data for matching documents.
    """
    if not os.path.exists(OUTPUT_JSON_PATH):
        print("[ERROR] output.json not found. Run the pipeline first: python main.py")
        return

    with open(OUTPUT_JSON_PATH, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    def do_search(query: str):
        print(f"\n Searching: \"{query}\"\n")
        results = search_documents(query, output_data, top_k=5)

        if not results:
            print("  No results found.")
            return

        for r in results:
            print(f"  Rank #{r['rank']} — {r['filename']}  (score: {r['score']})")
            print(json.dumps(r["data"], indent=4))
            print()

    if direct_query:
        do_search(direct_query)
    else:
        print("=" * 55)
        print("  DocuSort — Search Mode  (type 'exit' to quit)")
        print("=" * 55)
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() in ("exit", "quit", "q"):
                    break
                if not query:
                    continue
                do_search(query)
            except KeyboardInterrupt:
                print("\nExiting.")
                break


# Entry Point

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "search":
        direct_query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        run_search(direct_query)
    else:
        run_pipeline()
