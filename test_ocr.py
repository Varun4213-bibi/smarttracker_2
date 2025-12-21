import re
import datetime
from dateutil.parser import parse as dateutil_parse

def correct_ocr_text(text):
    """
    Correct common OCR misreads in expiry date text for medicine, groceries, and food labels.
    Includes context-aware replacements.
    """
    # Normalize and clean
    cleaned = text.replace('\n',' ').replace('\r',' ').upper()

    # Expanded corrections dictionary
    corrections = {
        # Month corrections
        "5EP": "SEP",
        "0CT": "OCT",
        "N0V": "NOV",
        "JULY": "JUL",
        "AUGUST": "AUG",
        "SEPTEMBER": "SEP",
        "NOVEMBER": "NOV",
        "DECEMBER": "DEC",
        "JAN1": "JAN",
        # Expiry prefixes
        "E3P": "EXP",
        "EXR": "EXP",
        "EXPIRY": "EXP",
        "EXPIRES": "EXP",
        "BEST BEFORE": "BB",
        "USE BY": "UB",
        "MFG": "MFG",
        "LOT": "LOT",
        # Numbers and symbols
        "O": "0",  # Use with caution
        "S": "5",  # For 5 in dates
        "Z": "2",  # For 2
        "B": "8",  # For 8
        "I": "1",  # For 1
        # Separators
        "|": "/",
        "·": ".",
        # Additional common misreads
        "EXPIRY DATE": "EXP",
        "BEST BY DATE": "BB",
        "USE BY DATE": "UB",
        "MANUFACTURED": "MFG",
        "BATCH": "LOT",
        "PRODUCED": "MFG",
        "PACKED": "MFG",
    }

    # Apply general corrections
    for wrong, right in corrections.items():
        cleaned = cleaned.replace(wrong, right)

    # Context-aware replacements: only replace if near date-related words
    date_keywords = ["EXP", "BB", "UB", "MFG", "LOT"]
    for keyword in date_keywords:
        if keyword in cleaned:
            # Replace numbers only in proximity to keywords (within 10 chars)
            start = cleaned.find(keyword)
            if start != -1:
                end = start + len(keyword) + 10
                segment = cleaned[start:end]
                # Apply number corrections in this segment
                segment = segment.replace("O", "0").replace("S", "5").replace("Z", "2").replace("B", "8").replace("I", "1")
                cleaned = cleaned[:start] + segment + cleaned[end:]

    return cleaned

# Simulate the corrected text from the screenshot
extracted_text = "LOT: EXP: 39 BAR 2024-03-10 MFG: NH49509-25-09 LOT:"
corrected = correct_ocr_text(extracted_text)

print("Corrected text:", repr(corrected))

patterns = [
    r'(EXP|BB|UB)[\s\:\.\-]*([1-2][0-9]{3})[\/\-\.][0-1][0-9][\/\-\.][0-3][0-9]',
    r'(EXP|BB|UB)[\s\w]*([0-1][0-9])\/([0-3][0-9])\/([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\w]*([0-3][0-9])\/([0-1][0-9])\/([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\:\.\-]*([A-Z]{3})[\s\.\:,]*([1-2][0-9]{3})\b',
    r'\b([A-Z]{3})[\.\s\:\-,]*([1-2][0-9]{3})\b',
    r'(EXP|BB|UB)[\s\:\.\-]*([01][0-9])[\/\.:\-\s]*([1-2][0-9]{3})',
    r'([01][0-9])[\/\.:\-\s]*([1-2][0-9]{3})',
    r'([1-2][0-9]{3})[\/\.:\-\s]*([01][0-9])',
    r'([0-3][0-9])[\/\-\.][0-1][0-9][\/\-\.][1-2][0-9]{3}',
    r'([0-1][0-9])[\/\-\.][0-3][0-9][\/\-\.][1-2][0-9]{3}',
    r'([0-3][0-9])\s+([0-1][0-9])\s+([1-2][0-9]{3})',
    r'([0-1][0-9])\s+([0-3][0-9])\s+([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\:\.\-]*([A-Z]{3})[\s\.\:,]*([0-9]{2})\b',
    r'\b([A-Z]{3})[\.\s\:\-,]*([0-9]{2})\b',
    r'(EXP|BB|UB)[\s\:\.\-]*([01][0-9])[\/\.:\-\s]*([0-9]{2})',
    r'([01][0-9])[\/\.:\-\s]*([0-9]{2})',
    r'([0-9]{2})[\/\.:\-\s]*([01][0-9])',
    r'([0-3][0-9])[\/\-\.][0-1][0-9][\/\-\.][0-9]{2}',
    r'([0-1][0-9])[\/\-\.][0-3][0-9][\/\-\.][0-9]{2}',
    r'([0-3][0-9])\s+([0-1][0-9])\s+([0-9]{2})',
    r'([0-1][0-9])\s+([0-3][0-9])\s+([0-9]{2})',
    r'(EXP|BB|UB)[\s\:\.\-]*([1-2][0-9]{3})',
    r'([0-3][0-9])\.([0-1][0-9])\.([1-2][0-9]{3})',
    r'\b([5S][EP][F])[\.\s\:\-\,]*([1-2][0-9]{3})\b',
    r'[E3][XK][P8][\s\:\.\-]*([A-Z0-9]{3})[\.\s\:\-\,]*([1-2][0-9]{3})\b',
    r'\b([5S][EP][F])[\.\s\:\-\,]*([0-9]{2})\b',
    r'[E3][XK][P8][\s\:\.\-]*([A-Z0-9]{3})[\.\s\:\-\,]*([0-9]{2})\b',
    r'([0-3]?[0-9]?)[\/\-\.]?([0-1]?[0-9]?)[\/\-\.]?([0-9]{2,4})',
]

current_year = 2024
current_two_digit = current_year % 100
valid_months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
possible_dates = []
today = datetime.date(2024, 10, 1)  # Assume current date after March 2024

print("\n=== Testing Patterns ===")

for pattern in patterns:
    matches = list(re.finditer(pattern, corrected, re.IGNORECASE))
    if matches:
        print(f"Pattern {pattern} found {len(matches)} matches")
        for m in matches:
            groups = m.groups()
            print(f"  Match: {m.group(0)}, Groups: {groups}")

# Optimized logic: Prioritize EXP-prefixed dates and limit parsing attempts
possible_dates = []

# First, look for EXP-prefixed dates specifically
exp_patterns = [
    r'(EXP|BB|UB)[\s\:\.\-]*([1-2][0-9]{3})[\/\-\.][0-1][0-9][\/\-\.][0-3][0-9]',
    r'(EXP|BB|UB)[\s\:\.\-]*([A-Z]{3})[\s\.\:,]*([1-2][0-9]{3})\b',
    r'(EXP|BB|UB)[\s\:\.\-]*([01][0-9])[\/\.:\-\s]*([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\:\.\-]*([A-Z]{3})[\s\.\:,]*([0-9]{2})\b',
    r'(EXP|BB|UB)[\s\:\.\-]*([01][0-9])[\/\.:\-\s]*([0-9]{2})',
]

date_candidates = []

# Prioritize EXP-prefixed matches
for pattern in exp_patterns:
    for match in re.finditer(pattern, corrected, re.IGNORECASE):
        full_match = match.group(0).strip()
        date_candidates.append(full_match)

# If no EXP-prefixed dates, fall back to general patterns but limit to top 5 candidates
if not date_candidates:
    for pattern in patterns[:10]:  # Limit to first 10 patterns for speed
        for match in re.finditer(pattern, corrected, re.IGNORECASE):
            full_match = match.group(0).strip()
            date_candidates.append(full_match)
            if len(date_candidates) >= 5:  # Limit candidates
                break
        if len(date_candidates) >= 5:
            break

# Remove duplicates
date_candidates = list(set(date_candidates))

print(f"\nDate candidates: {date_candidates}")

# Parse each candidate with dateutil (limit attempts)
for candidate in date_candidates[:5]:  # Limit parsing to top 5
    try:
        # Try US format first (MM/DD/YYYY)
        parsed = dateutil_parse(candidate, fuzzy=True, dayfirst=False)
        candidate_date = parsed.date()
        if current_year - 2 <= candidate_date.year <= current_year + 10:
            possible_dates.append(candidate_date)
            print(f"Parsed candidate: {candidate} -> {candidate_date}")
    except (ValueError, TypeError):
        try:
            # Try European format (DD/MM/YYYY)
            parsed = dateutil_parse(candidate, fuzzy=True, dayfirst=True)
            candidate_date = parsed.date()
            if current_year - 2 <= candidate_date.year <= current_year + 10:
                possible_dates.append(candidate_date)
                print(f"Parsed candidate (dayfirst): {candidate} -> {candidate_date}")
        except (ValueError, TypeError):
            continue

# Select the latest plausible date
print("\nPossible dates:", [d.isoformat() for d in possible_dates])
if possible_dates:
    expiry_date_obj = max(possible_dates)
    print("Selected expiry:", expiry_date_obj.isoformat())
else:
    print("No expiry found")
