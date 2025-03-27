import re


def extract_available(text):
    match = re.search(r"Available\s*-\s*\$?([\d.]+)", text)
    return float(match.group(1)) if match else 0
