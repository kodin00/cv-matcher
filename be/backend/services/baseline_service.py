from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_INDONESIAN_STOPWORDS = {
    "dan", "atau", "yang", "di", "ke", "dari", "untuk", "dengan", "pada",
    "adalah", "ini", "itu", "juga", "tidak", "akan", "sudah", "saya",
    "kami", "kita", "mereka", "anda", "serta", "dalam", "oleh", "karena",
    "sebagai", "setelah", "sebelum", "antara", "bahwa", "dapat", "lebih",
    "telah", "bagi", "seperti", "saat", "hingga", "selama", "melalui",
    "memiliki", "melakukan", "terhadap", "sangat", "namun", "ketika",
}


def compute_keyword_score(cv_text: str, jd_text: str) -> float:
    if not cv_text.strip() or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words=list(_INDONESIAN_STOPWORDS),
        sublinear_tf=True,
        token_pattern=r"(?u)\b\w+\b",
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([cv_text, jd_text])
    except ValueError:
        return 0.0

    if tfidf_matrix.shape[1] == 0:
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2]).item()
    return round(max(0.0, similarity) * 100.0, 2)


def build_score_comparison(semantic_score: float, keyword_score: float) -> dict:
    return {
        "semantic_score": semantic_score,
        "keyword_score":  keyword_score,
        "improvement":    round(semantic_score - keyword_score, 2),
    }
