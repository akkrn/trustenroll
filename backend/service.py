import re


def extract_available(card):
    match = re.search(r"[-]\s([\d,]+)\$", card)
    if match:
        return int(match.group(1).replace(",", ""))
    return 0
