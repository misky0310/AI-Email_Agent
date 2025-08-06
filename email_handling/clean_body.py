import re
from bs4 import BeautifulSoup

DISCLAIMER_PATTERNS = [
    r"\*\*Disclaimer:.*?(?=\n|$)",  # **Disclaimer: ...
    r"This message was sent from .*?Vellore Institute.*",  # Institute disclaimers
    r"Vellore Institute of Technology.*?(?=\n|$)",  # VIT promotional lines
    r"If you are not the intended recipient.*",  # Legal footer
    r"This email and any files transmitted with it.*",  # Legal footer
    r"Please do not print this email.*",  # Environmental notice
    r"^\s*--\s*$",  # Signature line (like "-- ")
    r"[*\-_]{2,}.*?(?=\n|$)",  # Lines with only asterisks or dashes (decorative)
    r"Warm regards.*?(?=\n|$)",  # Signature block
    r"Dr\.\s[Vv]\.?\s?Samuel Rajkumar.*?(?=\n|$)",  # Specific director signature
    r"\*?ALL THE BEST\*?",  # Motivational footer
    r"\(\s?QS World University Rankings.*?\)",  # QS ranking notes
    r"\*?Engineering and Technology:.*?(?=\n|$)",  # Specific promotional start
    r"\*?\d+(st|nd|rd|th)\s+best .*?India.*?(?=\n|$)",  # NIRF/ARWU ranks
    r"NAAC\*\*? Accreditation.*?(?=\n|$)",  # NAAC line
    r"\*?\d{3,}(?:th)? in the world.*?(?=\n|$)",  # Global ranks
]

def clean_disclaimer(text):
    for pattern in DISCLAIMER_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()

def strip_html(text):
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    except Exception:
        return text

def clean_email_body(body):
    body = strip_html(body)
    body = clean_disclaimer(body)
    body = re.sub(r"\n\s*\n", "\n\n", body,flags=re.IGNORECASE)  # normalize blank lines
    body = re.sub(r"\s{2,}", " ", body,flags=re.IGNORECASE)  # remove extra spaces
    return body.strip()

