# STUB -- replace with real sentence-transformers logic later

_model_loaded = False  # Will be set True when real model is loaded


def get_model():
    return None  # Stub: no model


def section_score(text_a: str, text_b: str) -> float:
    """Stub: always returns 50.0. Replace with real cosine similarity."""
    if not text_a.strip() or not text_b.strip():
        return 0.0
    return 50.0


def compute_match(cv_sections: dict, jd: dict) -> dict:
    """Stub: returns equal mock scores across all sections."""
    skills_score = section_score(cv_sections["skills"], " ".join(jd["required_skills"]))
    experience_score = section_score(cv_sections["experience"], jd["description"])
    education_score = section_score(cv_sections["education"], jd.get("required_education", ""))

    semantic = (skills_score * 0.4) + (experience_score * 0.4) + (education_score * 0.2)

    return {
        "semantic_score": round(semantic, 2),
        "skills_score": skills_score,
        "experience_score": experience_score,
        "education_score": education_score,
    }
