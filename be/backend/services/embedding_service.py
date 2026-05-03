from __future__ import annotations

from config import MODEL_NAME
from sentence_transformers import SentenceTransformer, util


_model = None
_model_loaded = False


def is_model_loaded() -> bool:
    return _model_loaded


def get_model() -> SentenceTransformer:
    global _model, _model_loaded

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
        _model_loaded = True
    return _model


def chunk_text(text: str, max_tokens: int = 128, overlap: int = 20) -> list[str]:
    tokens = text.split()
    if not tokens:
        return []
    if max_tokens <= 0:
        raise ValueError("max_tokens must be greater than 0.")
    if overlap < 0:
        raise ValueError("overlap must not be negative.")
    if overlap >= max_tokens:
        raise ValueError("overlap must be smaller than max_tokens.")

    if len(tokens) <= max_tokens:
        return [" ".join(tokens)]

    step = max_tokens - overlap
    chunks = []
    for start in range(0, len(tokens), step):
        chunk_tokens = tokens[start:start + max_tokens]
        if not chunk_tokens:
            break
        chunks.append(" ".join(chunk_tokens))
        if start + max_tokens >= len(tokens):
            break
    return chunks


def section_score(text_a: str, text_b: str) -> float:
    if not text_a.strip() or not text_b.strip():
        return 0.0

    chunks_a = chunk_text(text_a)
    chunks_b = chunk_text(text_b)
    if not chunks_a or not chunks_b:
        return 0.0

    model = get_model()
    all_chunks = chunks_a + chunks_b
    embeddings = model.encode(
        all_chunks,
        convert_to_tensor=True,
        show_progress_bar=False,
    )

    embeddings_a = embeddings[:len(chunks_a)]
    embeddings_b = embeddings[len(chunks_a):]
    pooled_a = embeddings_a.mean(dim=0, keepdim=True)
    pooled_b = embeddings_b.mean(dim=0, keepdim=True)

    similarity = util.cos_sim(pooled_a, pooled_b).item()
    return round(max(0.0, similarity) * 100.0, 2)


def compute_match(cv_sections: dict, jd: dict) -> dict:
    skills_score = section_score(cv_sections["skills"], " ".join(jd["required_skills"]))
    experience_score = section_score(cv_sections["experience"], jd["description"])
    education_score = section_score(cv_sections["education"], jd.get("required_education", ""))

    semantic = (skills_score * 0.4) + (experience_score * 0.4) + (education_score * 0.2)

    return {
        "semantic_score": round(float(semantic), 2),
        "skills_score": float(skills_score),
        "experience_score": float(experience_score),
        "education_score": float(education_score),
    }
