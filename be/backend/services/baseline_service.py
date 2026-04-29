# STUB -- replace compute_keyword_score with real TfidfVectorizer logic later

def compute_keyword_score(cv_text: str, jd_text: str) -> float:
    """Stub: returns mock keyword score."""
    if not cv_text.strip() or not jd_text.strip():
        return 0.0
    return 30.0  # mock


def build_score_comparison(semantic_score: float, keyword_score: float) -> dict:
    """Assemble the score_comparison block returned in every /api/match result."""
    return {
        "semantic_score": semantic_score,
        "keyword_score": keyword_score,
        "improvement": round(semantic_score - keyword_score, 2),
    }
