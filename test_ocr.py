import re
import datetime

# Simulate the corrected text from the screenshot
extracted_text = "LOT: EXP: 39 BAR 2024-03-10 MFG: NH49509-25-09 LOT:"
cleaned = extracted_text.replace('\n',' ').replace('\r',' ').upper()
corrected = (cleaned
    .replace("5EP", "SEP")
    .replace("0CT", "OCT")
    .replace("N0V", "NOV")
    .replace("JULY", "JUL")
    .replace("AUGUST", "AUG")
    .replace("SEPTEMBER", "SEP")
    .replace("NOVEMBER", "NOV")
    .replace("DECEMBER", "DEC")
    .replace("JAN1", "JAN")
    .replace("E3P", "EXP").replace("EXR", "EXP")
    .replace("EXPIRY", "EXP")
    .replace("EXPIRES", "EXP")
    .replace("BEST BEFORE", "BB")
    .replace("USE BY", "UB")
    .replace("MFG", "MFG")
    .replace("LOT", "LOT")
    .replace("O", "0")
    .replace("S", "5")
    .replace("Z", "2")
    .replace("B", "8")
    .replace("I", "1")
    .replace("|", "/")
    .replace("·", ".")
)

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

# Now run the full logic
possible_dates = []
for pattern in patterns:
    for match in re.finditer(pattern, corrected, re.IGNORECASE):
        groups = match.groups()
        if len(groups) >= 2:
            candidate_date = None
            # Handle prefixed 4-group patterns
            if len(groups) == 4 and groups[0] and groups[0].upper() in ['EXP', 'BB', 'UB']:
                prefix, g1, g2, g3 = groups
                try:
                    if len(g3) == 4 and g3.isdigit():  # year last
                        part1_str, part2_str, year_str = g1, g2, g3
                        p1 = int(part1_str)
                        p2 = int(part2_str)
                        year_int = int(year_str)
                        if current_year - 2 <= year_int <= current_year + 10:
                            if p1 <= 12 and p1 >= 1:
                                month_int, day_int = p1, p2
                            else:
                                month_int, day_int = p2, p1
                            if 1 <= month_int <= 12 and 1 <= day_int <= 31:
                                candidate_date = datetime.date(year_int, month_int, day_int)
                    else:  # year first YYYY-MM-DD
                        year_str, month_str, day_str = g1, g2, g3
                        year_int = int(year_str)
                        month_int = int(month_str)
                        day_int = int(day_str)
                        if 1 <= month_int <= 12 and 1 <= day_int <= 31 and current_year - 2 <= year_int <= current_year + 10:
                            candidate_date = datetime.date(year_int, month_int, day_int)
                except ValueError:
                    continue
            # Handle full date patterns (3 groups)
            elif len(groups) == 3:
                part1, part2, year_str = [g for g in groups if g is not None]
                if part1 and part2 and year_str:
                    try:
                        p1 = int(part1)
                        p2 = int(part2)
                        year_int = int(year_str)
                        if len(year_str) == 2:
                            base_year = 2000 + year_int
                            if year_int < (current_year % 100) - 10:
                                base_year = 1900 + year_int
                            full_year = base_year
                        else:
                            full_year = year_int
                        if current_year - 2 <= full_year <= current_year + 10:
                            if p1 <= 12 and p1 >= 1:
                                month, day = p1, p2
                            else:
                                month, day = p2, p1
                            if 1 <= month <= 12 and 1 <= day <= 31:
                                candidate_date = datetime.date(full_year, month, day)
                    except ValueError:
                        continue
            else:
                # Month/year patterns
                digit_groups = [g for g in groups if g and g.isdigit()]
                if len(digit_groups) >= 2:
                    g1, g2 = digit_groups[0], digit_groups[1]
                    if g1 and g2:
                        # year-month 4-2
                        if len(g1) == 4 and 2000 <= int(g1) <= 2035 and len(g2) == 2 and 1 <= int(g2) <= 12:
                            try:
                                candidate_date = datetime.date(int(g1), int(g2), 1)
                            except ValueError:
                                pass
                        # month-year 2-4
                        elif len(g1) == 2 and 1 <= int(g1) <= 12 and len(g2) == 4 and 2000 <= int(g2) <= 2035:
                            try:
                                candidate_date = datetime.date(int(g2), int(g1), 1)
                            except ValueError:
                                pass
                        # 2-digit year-month
                        elif len(g1) == 2 and len(g2) == 2 and 1 <= int(g2) <= 12:
                            year_int = int(g1)
                            month_int = int(g2)
                            if year_int >= current_two_digit - 2 and year_int <= current_two_digit + 10:
                                full_year = 2000 + year_int
                                try:
                                    candidate_date = datetime.date(full_year, month_int, 1)
                                except ValueError:
                                    pass
                        # 2-digit month-year
                        elif len(g1) == 2 and 1 <= int(g1) <= 12 and len(g2) == 2:
                            year_int = int(g2)
                            month_int = int(g1)
                            if year_int >= current_two_digit - 2 and year_int <= current_two_digit + 10:
                                full_year = 2000 + year_int
                                try:
                                    candidate_date = datetime.date(full_year, month_int, 1)
                                except ValueError:
                                    pass
                # 3-letter month + year
                month_str = next((g for g in groups if g and len(g) <= 3 and g.isalpha()), None)
                if month_str:
                    month = month_str.upper()
                    year_str = next((g for g in groups if g and g.isdigit()), None)
                    if year_str:
                        try:
                            year_int = int(year_str)
                            if len(year_str) == 2:
                                if year_int >= current_two_digit - 2 and year_int <= current_two_digit + 10:
                                    full_year = 2000 + year_int
                                else:
                                    full_year = 2000 + year_int
                            else:
                                full_year = year_int
                            if current_year - 2 <= full_year <= current_year + 10 and month in valid_months:
                                month_num = valid_months.index(month) + 1
                                candidate_date = datetime.date(full_year, month_num, 1)
                        except (ValueError, IndexError):
                            pass

            if candidate_date:
                if candidate_date > today or (len(possible_dates) == 0 and current_year - 2 <= candidate_date.year <= current_year + 5):
                    possible_dates.append(candidate_date)
                    print(f"Added candidate: {candidate_date}")

print("\nPossible dates:", [d.isoformat() for d in possible_dates])
if possible_dates:
    expiry_date_obj = max(possible_dates)
    print("Selected expiry:", expiry_date_obj.isoformat())
else:
    print("No expiry found")
