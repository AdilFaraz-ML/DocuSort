# Keywords are written per category — order by specificity (more specific first)
INVOICE_KEYWORDS = [
    "invoice number", "inv-", "invoice no", "bill to", "sold to",
    "invoice", "subtotal", "tax", "total amount", "payment due",
    "amount due", "purchase order", "po number", "vendor",
    "remit to", "net 30", "net 60", "due date", "item description"
]

RESUME_KEYWORDS = [
    "curriculum vitae", "work experience", "professional experience",
    "career objective", "summary of qualifications", "references available",
    "resume", "objective", "education", "skills", "employment",
    "work history", "certifications", "achievements", "languages",
    "projects", "internship", "bachelor", "master", "gpa"
]

UTILITY_KEYWORDS = [
    "kwh", "kilowatt", "meter number", "meter reading", "account number",
    "bill period", "billing period", "electricity", "utility", "gas bill",
    "water bill", "consumption", "usage", "current charges",
    "previous balance", "service address", "tariff", "units consumed"
]

SCORE_THRESHOLD = 1  


def score_text(text: str, keywords: list) -> int:
    """Count how many keywords appear in the text."""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw in text_lower)


def classify_document(text: str) -> str:
    """
    Classify a document based on keyword frequency.

    Returns:
        str: One of Invoice | Resume | Utility Bill | Other | Unclassifiable
    """
    if not text or len(text.strip()) < 50:
        return "Unclassifiable"

    scores = {
        "Invoice":      score_text(text, INVOICE_KEYWORDS),
        "Resume":       score_text(text, RESUME_KEYWORDS),
        "Utility Bill": score_text(text, UTILITY_KEYWORDS),
    }

    best_class = max(scores, key=scores.get)
    best_score = scores[best_class]

    if best_score == 0:
        return "Unclassifiable"
    elif best_score < SCORE_THRESHOLD:
        return "Other"
    else:
        return best_class
