import re
import datetime

def correct_ocr_text(text):
    cleaned = text.replace('\n',' ').replace('\r',' ').upper()
    corrections = {
        "5EP": "SEP", "0CT": "OCT", "N0V": "NOV", "JULY": "JUL", "AUGUST": "AUG",
        "SEPTEMBER": "SEP", "NOVEMBER": "NOV", "DECEMBER": "DEC", "JAN1": "JAN",
        "E3P": "EXP", "EXR": "EXP", "EXPIRY": "EXP", "EXPIRES": "EXP",
        "BEST BEFORE": "BB", "USE BY": "UB", "MFG": "MFG", "LOT": "LOT",
        "DAIE": "DATE", "MRE": "MFG", "USEBV": "UB", "USE BV": "UB", "BV": "BY", "VSE": "USE",
        "UKSE": "USE", "UK5E": "USE", "U5E": "USE", "8Y": "BY",
        "O": "0", "S": "5", "Z": "2", "B": "8", "I": "1", "|": "/", "·": ".", "\\": "/",
        "EXPIRY DATE": "EXP", "BEST BY DATE": "BB", "USE BY DATE": "UB",
        "MANUFACTURED": "MFG", "BATCH": "LOT", "PRODUCED": "MFG", "PACKED": "MFG",
        "USEBY": "UB", "EXP.": "EXP", "MFG.": "MFG",
    }
    for wrong, right in corrections.items():
        cleaned = cleaned.replace(wrong, right)

    date_keywords = ["EXP", "BB", "UB", "MFG", "LOT", "DATE", "BY", "BV"]
    for keyword in date_keywords:
        if keyword in cleaned:
            start = cleaned.find(keyword)
            if start != -1:
                end = start + len(keyword) + 20
                segment = cleaned[start:end]
                segment = segment.replace("O", "0").replace("S", "5").replace("Z", "2").replace("I", "1")
                if not re.search(r'202[B]', segment):
                     segment = segment.replace("B", "8")
                cleaned = cleaned[:start] + segment + cleaned[end:]
    return cleaned

patterns = [
    r'(EXP|BB|UB)[\s\:\.\-]*([1-2][0-9]{3})[\/\-\.][0-1][0-9][\/\-\.][0-3][0-9]',
    r'([1-2][0-9]{3})[\/\-\.][0-1][0-9][\/\-\.][0-3][0-9]',
    r'(EXP|BB|UB)\s*([0-1][0-9])\/([0-3][0-9])\/([1-2][0-9]{3})',
    r'(EXP|BB|UB)\s*([0-3][0-9])\/([0-1][0-9])\/([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\w]*([0-1][0-9])\/([0-3][0-9])\/([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\w]*([0-3][0-9])\/([0-1][0-9])\/([1-2][0-9]{3})',
    r'(EXP|BB|UB)\s*([0-1][0-9])\/([0-3][0-9])\/([0-9]{2})',
    r'(EXP|BB|UB)\s*([0-3][0-9])\/([0-1][0-9])\/([0-9]{2})',
    r'(EXP|BB|UB)[\s\:\.\-]*([0-3][0-9])([0-1][0-9])([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\:\.\-]*([0-3][0-9])([0-1][0-9])([0-9]{2})',
    r'(EXP|BB|UB|DATE|BY|BV)[\s\:\.\-]*([0-3][0-9])1([0-1][0-9])1([1-2][0-9]{3})',
    r'(EXP|BB|UB|DATE|BY|BV)[\s\:\.\-]*(\d{8,10})',
    r'(EXP|BB|UB)[\s\:\.\-]*([A-Z]{3})[\s\.\:,]*([1-2][0-9]{3})\b',
    r'\b([A-Z]{3})[\.\s\:\-,]*([1-2][0-9]{3})\b',
    r'(EXP|BB|UB)[\s\:\.\-]*([01][0-9])[\/\.:\-\s]*([1-2][0-9]{3})',
    r'\b([01][0-9])[\/\.:\-\s]*([1-2][0-9]{3})\b',
    r'\b([1-2][0-9]{3})[\/\.:\-\s]*([01][0-9])\b',
    r'\b([0-3][0-9])[\/\-\.][0-1][0-9][\/\-\.][1-2][0-9]{3}\b',
    r'\b([0-1][0-9])[\/\-\.][0-3][0-9][\/\-\.][1-2][0-9]{3}\b',
    r'([0-3][0-9])\s+([0-1][0-9])\s+([1-2][0-9]{3})',
    r'([0-1][0-9])\s+([0-3][0-9])\s+([1-2][0-9]{3})',
    r'(EXP|BB|UB)[\s\:\.\-]*([A-Z]{3})[\s\.\:,]*([0-9]{2})\b',
    r'\b([A-Z]{3})[\.\s\:\-,]*([0-9]{2})\b',
    r'(EXP|BB|UB)[\s\:\.\-]*([01][0-9])[\/\.:\-\s]*([0-9]{2})',
    r'\b([01][0-9])[\/\.:\-\s]*([0-9]{2})\b',
    r'\b([0-9]{2})[\/\.:\-\s]*([01][0-9])\b',
    r'\b([0-3][0-9])[\/\-\.][0-1][0-9][\/\-\.][0-9]{2}\b',
    r'\b([0-1][0-9])[\/\-\.][0-3][0-9][\/\-\.][0-9]{2}\b',
    r'([0-3][0-9])\s+([0-1][0-9])\s+([0-9]{2})',
    r'([0-1][0-9])\s+([0-3][0-9])\s+([0-9]{2})',
    r'(EXP|BB|UB)[\s\:\.\-]*([1-2][0-9]{3})',
    r'([0-3][0-9])\.([0-1][0-9])\.([1-2][0-9]{3})',
    r'([0-3][0-9])\.([0-1][0-9])\s+([1-2][0-9]{3})',
    r'([0-3][0-9])\,([0-1][0-9])\,([1-2][0-9]{3})',
    r'(EXP|BB|UB)\:\s*([0-3][0-9])\.([0-1][0-9])\,([1-2][0-9]{3})',
    r'\b([5S][EP][F])[\.\s\:\-\,]*([1-2][0-9]{3})\b',
    r'[E3][XK][P8][\s\:\.\-]*([A-Z0-9]{3})[\.\s\:\-\,]*([1-2][0-9]{3})\b',
    r'\b([5S][EP][F])[\.\s\:\-\,]*([0-9]{2})\b',
    r'[E3][XK][P8][\s\:\.\-]*([A-Z0-9]{3})[\.\s\:\-\,]*([0-9]{2})\b',
    r'\b([0-3]?[0-9])[\/\-\.]([0-1]?[0-9])[\/\-\.](202[4-9]|203[0-5]|2[4-9]|3[0-5])\b',
]

text = "C0NTA1NE MUT TL AND} DRY PLACE: 00FTTGERAT0  0' FEGHNE5E, D0 N0T ACCCPL 1F EEAL LE TAM 0 12 NATURE/ PR0CE55 1TD0E5RTU AFLEC DA 0 51TY 1N 0NY WAY: MLX 1T WELL 8EL0RE U5E, M 4 100 3 N0LUR0L PEANUT 0, EK5EL MM 51URE VME JWAR UP51DE D0WW {@AVQ1D 01L 5EPARAT10H: FER FEED8ACK, C0NTACT 0UR CU5T0MER CARE EXECUT1VE AT THE MARKETED 8Y ADDRE55 CALL 1800274-7144. 15UPP0RT@P1NT0LA1 1N FR0DUCT 0F  (RACD18L0 1ND1A HRP 7 399.00 (UNK 5  PRCERDERG E8&T2T 8ATCH N0: 32350220 HFG DATE: 23/08/2023 UKSE BY: 2210212025 USFDYA 150 RAE0N RAN1TD 01N0 RAUANNUUT KHYMALL0N' ELTER= '0PENHP 1PERCA JL1AN N0LHLNG JU5T"

corrected = correct_ocr_text(text)
print("Corrected:", corrected)

current_year = 2026
current_two_digit = 26
today = datetime.date(2026, 2, 5)
valid_months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
possible_dates_with_scores = []

for p in patterns:
    for match in re.finditer(p, corrected, re.IGNORECASE):
        groups = match.groups()
        candidate_date = None
        score = 0
        
        # Mimic logic for 4 groups
        if len(groups) == 4 and groups[0] and groups[0].upper() in ['EXP', 'BB', 'UB', 'DATE', 'BY', 'BV']:
            prefix, g1, g2, g3 = groups
            score = 12
            try:
                if g3.isdigit():
                    p1, p2, year_str = int(g1), int(g2), g3
                    if len(year_str) == 4:
                        year_int = int(year_str)
                        if 1 <= p1 <= 12 and 1 <= p2 <= 31: candidate_date = datetime.date(year_int, p1, p2)
                        elif 1 <= p2 <= 12 and 1 <= p1 <= 31: candidate_date = datetime.date(year_int, p2, p1)
                    elif len(year_str) == 2:
                        year_int = 2000 + int(year_str)
                        if 1 <= p1 <= 12 and 1 <= p2 <= 31: candidate_date = datetime.date(year_int, p1, p2)
                        elif 1 <= p2 <= 12 and 1 <= p1 <= 31: candidate_date = datetime.date(year_int, p2, p1)
                        score = 10
            except: pass

        elif len(groups) == 3:
            g1, g2, g3 = groups
            if g1 and g2 and g3 and g1.strip() and g2.strip() and g3.strip():
                score = 10
                try:
                    p1, p2, p3 = int(g1), int(g2), int(g3)
                    if p3 > 2000: candidate_date = datetime.date(p3, p2, p1) # Simple assumption for repro
                    else: candidate_date = datetime.date(2000+p3, p2, p1)
                except: pass
        
        elif len(groups) == 2:
            if groups[0] and groups[0].upper() in ['EXP', 'BB', 'UB', 'DATE', 'BY', 'BV'] and groups[1].isdigit():
                digits = groups[1]
                score = 9
                try:
                    if len(digits) == 8:
                        p1, p2, yr = int(digits[:2]), int(digits[2:4]), int(digits[4:])
                        candidate_date = datetime.date(yr, p1, p2)
                    elif len(digits) == 10:
                        d, m, y = int(digits[:2]), int(digits[3:5]), int(digits[6:])
                        candidate_date = datetime.date(y, m, d)
                        score = 11
                except: pass
            else:
                score = 5
                try:
                    p1, p2 = int(groups[0]), int(groups[1])
                    if p2 > 100: candidate_date = datetime.date(p2, p1, 1)
                    else: candidate_date = datetime.date(2000+p2, p1, 1)
                except: pass

        if candidate_date:
            possible_dates_with_scores.append((candidate_date, score))
            print(f"Found: {candidate_date} Score: {score}")

if possible_dates_with_scores:
    possible_dates_with_scores.sort(key=lambda x: (-x[1], x[0]))
    print("BEST:", possible_dates_with_scores[0])
