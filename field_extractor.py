import re


# Shared Patterns

DATE_PATTERN = re.compile(
    r'\b('
    r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}'          
    # 01/15/2025


    r'|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}'            
    # 2025-01-15


    r'|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*'
    r'\s+\d{1,2},?\s+\d{4}'                        
    # January 15, 2025


    r'|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*'
    r'\s+\d{4}'                                     
    # 15 January 2025


    r')\b',
    re.IGNORECASE
)


# Invoice Extraction

def extract_invoice_fields(text: str) -> dict:
    fields = {
        "invoice_number": None,
        "date":           None,
        "company":        None,
        "total_amount":   None,
    }

    # Invoice number
    inv_match = re.search(
        r'(?i)invoice\s*(?:no\.?|number|#|num)?[\s:\-]*([A-Z0-9][\w\-]{2,20})',
        text
    )
    if inv_match:
        fields["invoice_number"] = inv_match.group(1).strip()

    # Date
    date_match = DATE_PATTERN.search(text)
    if date_match:
        fields["date"] = date_match.group(1)

    company_match = re.search(
        r'(?i)(?:from|billed\s*by|company|vendor|seller|issued\s*by)[\s:\-]+([A-Z][^\n,\.]{2,50})',
        text
    )
    if company_match:
        fields["company"] = company_match.group(1).strip()
    else:
        # Fallback: grab the first all-caps line (many invoices have company name at top)
        caps_match = re.search(r'^([A-Z][A-Z\s\.\,&]{5,50})$', text, re.MULTILINE)
        if caps_match:
            fields["company"] = caps_match.group(1).strip()

    # Total amount
    total_match = re.search(
        r'(?i)(?:total\s*amount|grand\s*total|amount\s*due|total\s*due|total)[\s:\$]*([\d,]+\.?\d{0,2})',
        text
    )
    if total_match:
        try:
            fields["total_amount"] = float(total_match.group(1).replace(",", ""))
        except ValueError:
            pass

    return fields


# Resume Extraction

def extract_resume_fields(text: str) -> dict:
    fields = {
        "name":             None,
        "email":            None,
        "phone":            None,
        "experience_years": None,
    }

    # Email
    email_match = re.search(
        r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
        text
    )
    if email_match:
        fields["email"] = email_match.group()

    # Phone — handles international and local formats
    phone_match = re.search(
        r'(?:\+?\d{1,3}[\s\-\.]?)?'
        r'(?:\(?\d{2,4}\)?[\s\-\.]?)?'
        r'\d{3}[\s\-\.]\d{4,6}',
        text
    )
    if phone_match:
        fields["phone"] = phone_match.group().strip()

    

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    skip_keywords = {"resume", "curriculum vitae", "cv", "objective", "summary"}
    for line in lines[:5]:  
        # It will check only top 5 lines
        if line.lower() not in skip_keywords and len(line.split()) <= 5:
            fields["name"] = line
            break

    # Experience years — "5 years of experience", "3+ years", etc.
    exp_match = re.search(
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s*(?:experience|exp)',
        text,
        re.IGNORECASE
    )
    if exp_match:
        fields["experience_years"] = int(exp_match.group(1))

    return fields


# Utility Bill Extraction

def extract_utility_fields(text: str) -> dict:
    fields = {
        "account_number": None,
        "date":           None,
        "usage_kwh":      None,
        "amount_due":     None,
    }

    # Account number
    acc_match = re.search(
        r'(?i)account\s*(?:no\.?|number|#|num)?[\s:\-]+([A-Z0-9][\w\-]{3,20})',
        text
    )
    if acc_match:
        fields["account_number"] = acc_match.group(1).strip()

    # Date
    date_match = DATE_PATTERN.search(text)
    if date_match:
        fields["date"] = date_match.group(1)

    # kWh usage
    kwh_match = re.search(
        r'([\d,]+\.?\d*)\s*kwh',
        text,
        re.IGNORECASE
    )
    if kwh_match:
        try:
            fields["usage_kwh"] = float(kwh_match.group(1).replace(",", ""))
        except ValueError:
            pass

    # Amount due
    amount_match = re.search(
        r'(?i)(?:amount\s*due|total\s*due|total\s*amount|please\s*pay)[\s:\$Rs\.]*([\d,]+\.?\d{0,2})',
        text
    )
    if amount_match:
        try:
            fields["amount_due"] = float(amount_match.group(1).replace(",", ""))
        except ValueError:
            pass

    return fields


# Entry Point

def extract_fields(doc_class: str, text: str) -> dict:
    """
    Route to the correct extractor based on document class.

    Returns:
        dict of extracted fields, or {} for Other/Unclassifiable
    """
    if doc_class == "Invoice":
        return extract_invoice_fields(text)
    elif doc_class == "Resume":
        return extract_resume_fields(text)
    elif doc_class == "Utility Bill":
        return extract_utility_fields(text)
    else:
        return {}
