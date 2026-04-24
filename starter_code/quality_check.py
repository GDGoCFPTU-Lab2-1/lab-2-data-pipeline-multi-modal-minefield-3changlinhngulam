# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================

import re

# Strings that indicate corrupt/error data
TOXIC_PATTERNS = [
    r"null pointer exception",
    r"traceback \(most recent call last\)",
    r"error:",
    r"undefined",
    r"nan",
    r"n/a",
    r"liên hệ",   # "contact us" placeholder — not a real value
]

# Known logic discrepancies to flag (comment claim -> actual value)
KNOWN_DISCREPANCIES = [
    {
        "description": "legacy_tax_calc: comment claims 8% VAT but code applies 10%",
        "source_type": "Code",
        "keyword": "legacy_tax_calc",
    }
]


def _is_toxic(text: str) -> bool:
    """Return True if the content contains any toxic/error pattern."""
    lowered = text.lower()
    return any(re.search(p, lowered) for p in TOXIC_PATTERNS)


def _check_discrepancies(document_dict: dict) -> list[str]:
    """Return a list of discrepancy warning messages found in the document."""
    warnings = []
    content = document_dict.get("content", "").lower()
    source_type = document_dict.get("source_type", "")

    for rule in KNOWN_DISCREPANCIES:
        if rule["source_type"] == source_type and rule["keyword"].lower() in content:
            warnings.append(f"[DISCREPANCY] {rule['description']}")

    return warnings


def run_quality_gate(document_dict: dict) -> bool:
    """
    Returns True if the document passes all quality gates, False otherwise.
    Gates:
      1. content must be >= 20 characters
      2. content must not contain toxic/error strings
      3. flags (but does not reject) known logic discrepancies
    """
    content = document_dict.get("content", "")

    # Gate 1: minimum content length
    if len(content) < 20:
        print(f"[QA FAIL] Document '{document_dict.get('document_id')}' rejected: "
              f"content too short ({len(content)} chars).")
        return False

    # Gate 2: toxic content check
    if _is_toxic(content):
        print(f"[QA FAIL] Document '{document_dict.get('document_id')}' rejected: "
              f"toxic/error string detected in content.")
        return False

    # Gate 3: discrepancy flagging (warn, don't reject)
    warnings = _check_discrepancies(document_dict)
    for w in warnings:
        print(f"[QA WARN] Document '{document_dict.get('document_id')}': {w}")

    return True
