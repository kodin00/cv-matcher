import re
import unicodedata
from langdetect import detect, LangDetectException

ABBREV_MAP = {
    "manajer proyek": "project manager",
    "pengembang perangkat lunak": "software developer",
    "s1": "bachelor",
    "s2": "master",
    "s3": "doctorate",
    "smk": "vocational high school",
    "sma": "high school",
}


def normalize(text: str) -> str:
    """Normalize raw CV text: unicode normalization, whitespace collapse, strip, lowercase, abbreviation mapping."""
    # 1. Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # 2. Collapse multiple spaces/tabs into a single space
    text = re.sub(r'\s+', ' ', text)

    # 3. Strip leading/trailing whitespace
    text = text.strip()

    # 4. Lowercase
    text = text.lower()

    # 5. Apply abbreviation map
    for abbrev, replacement in ABBREV_MAP.items():
        text = text.replace(abbrev, replacement)

    return text


def detect_language(text: str) -> str:
    """Detect language of text by chunking on '.' and '\\n'. Returns 'id', 'en', 'bilingual', or 'unknown'."""
    if not text or not text.strip():
        return "unknown"

    # Split text into chunks by '.' and '\\n'
    chunks = re.split(r'[.\n]', text)

    detected_languages = set()

    for chunk in chunks:
        chunk = chunk.strip()
        # Skip chunks that are too short (min 10 chars to avoid noise)
        if len(chunk) < 10:
            continue
        try:
            lang = detect(chunk)
            detected_languages.add(lang)
        except LangDetectException:
            continue

    if not detected_languages:
        return "unknown"

    # Check for bilingual (both Indonesian and English detected)
    if "id" in detected_languages and "en" in detected_languages:
        return "bilingual"

    # Return the single dominant language
    return detected_languages.pop()
