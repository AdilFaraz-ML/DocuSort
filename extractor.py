import os
from pdfminer.high_level import extract_text as pdf_extract


def extract_text_from_pdf(filepath: str) -> str:
    """Extract raw text from a PDF file using pdfminer."""
    try:
        text = pdf_extract(filepath)
        return text.strip() if text else ""
    except Exception as e:
        print(f"  [WARNING] Could not read {filepath}: {e}")
        return ""


def extract_text_from_txt(filepath: str) -> str:
    """Read plain text file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    except Exception as e:
        print(f"  [WARNING] Could not read {filepath}: {e}")
        return ""


def load_documents(folder_path: str) -> dict:
    """
    Load all PDF and TXT files from the given folder.

    Returns:
        dict: { filename: raw_text }
    """
    documents = {}
    supported = (".pdf", ".txt")

    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder not found: {folder_path}")
        return documents

    files = sorted(f for f in os.listdir(folder_path) if f.lower().endswith(supported))

    if not files:
        print(f"[ERROR] No PDF or TXT files found in '{folder_path}'")
        return documents

    print(f"\n Found {len(files)} document(s) in '{folder_path}'")

    for filename in files:
        filepath = os.path.join(folder_path, filename)
        print(f"  → Loading: {filename}")

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(filepath)
        else:
            text = extract_text_from_txt(filepath)

        documents[filename] = text

    return documents
