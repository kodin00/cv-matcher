import re

# Compiled regex for bilingual section headings — word-boundary guards prevent mid-word matches
_HEADING_RE = re.compile(
    r'(?i)'  # case-insensitive
    r'(?<!\n)'  # not already preceded by a newline
    r'(?:'
    r'\b(?:skills?|keahlian|keterampilan|tech\s*skills?|technical\s*skills?)\b'
    r'|'
    r'\b(?:experience?|pengalaman|work\s*experience?|pengalaman\s*kerja)\b'
    r'|'
    r'\b(?:education?|pendidikan|educational\s*background|latar\s*belakang\s*pendidikan)\b'
    r'|'
    r'\b(?:name|nama)\b'
    r'|'
    r'\b(?:summary|ringkasan|profile|profil|objective|tujuan)\b'
    r'|'
    r'\b(?:certifications?|sertifikasi?|licenses?|lisensi)\b'
    r'|'
    r'\b(?:languages?|bahasa)\b'
    r'|'
    r'\b(?:projects?|proyek)\b'
    r')'
    r'(?!\n)'  # not already followed by a newline
)


SECTION_ANCHORS = {
    "skills": [
        "keahlian", "keterampilan", "kompetensi", "kemampuan",
        "skills", "competencies", "technical skills",
    ],
    "experience": [
        "pengalaman kerja", "pengalaman", "riwayat pekerjaan",
        "experience", "work history", "employment",
    ],
    "education": [
        "pendidikan", "riwayat pendidikan",
        "education", "academic background",
    ],
}


_EDU_PATTERNS = [
    (r'\b(s3|doctorate|doktor|phd)\b', "Doctorate"),
    (r'\b(s2|master|magister|m\.sc|msc)\b', "Master"),
    (r'\b(s1|bachelor|sarjana|b\.sc|bsc)\b', "Bachelor"),
    (r'\b(d3|diploma)\b', "Diploma"),
]

_EXP_PATTERN = re.compile(r'(\d+)\s*(?:tahun|year)', re.IGNORECASE)


def inject_section_breaks(text: str) -> str:
    """Insert newlines around section headings so flat OCR text becomes line-structured."""
    def _replace(match):
        heading = match.group(0)
        return f'\n{heading}\n'

    return _HEADING_RE.sub(_replace, text)


def segment_cv(text: str) -> dict:
    """Split CV text into skills/experience/education buckets with full-text fallback."""
    normalized = inject_section_breaks(text)
    buckets = {"skills": [], "experience": [], "education": []}
    current_section = None

    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lowered = line.lower()
        matched_section = next(
            (
                section
                for section, anchors in SECTION_ANCHORS.items()
                if any(anchor in lowered for anchor in anchors)
            ),
            None,
        )

        if matched_section:
            current_section = matched_section
            continue

        if current_section:
            buckets[current_section].append(line)

    # If a section has no captured lines, use the full normalized text for that section.
    return {
        section: (" ".join(lines) if lines else normalized)
        for section, lines in buckets.items()
    }


SKILL_LIST = [
    # English - Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
    "ruby", "php", "swift", "kotlin", "scala", "r", "rust", "perl", "dart",
    "matlab", "sas", "bash", "shell scripting", "powershell",

    # English - Web Development
    "html", "css", "react", "angular", "vue", "vue.js", "node.js", "django",
    "flask", "fastapi", "spring boot", "express", "next.js", "nuxt.js",
    "rest api", "graphql", "webpack", "sass", "tailwind css", "bootstrap",

    # English - Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "mssql", "sql server", "nosql", "elasticsearch", "cassandra", "dynamodb",

    # English - DevOps & Cloud
    "docker", "kubernetes", "aws", "gcp", "azure", "terraform", "jenkins",
    "gitlab ci", "github actions", "ansible", "linux", "nginx", "apache",

    # English - Data & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "data analysis", "data visualization", "data engineering", "etl",
    "statistics", "pandas", "numpy", "tableau", "power bi", "excel",
    "natural language processing", "computer vision", "mlops",

    # English - General
    "git", "agile", "scrum", "kanban", "ci/cd", "devops", "microservices",
    "api development", "unit testing", "integration testing", "tdd",
    "debugging", "code review", "system design", "architecture",
    "problem solving", "communication skills", "team leadership",
    "project management", "technical documentation",

    # English - Security & Networking
    "cybersecurity", "penetration testing", "network security", "firewall",
    "encryption", "authentication", "authorization", "oauth", "jwt",
    "networking", "tcp/ip", "dns", "http", "https",

    # English - Mobile
    "android", "ios", "flutter", "react native", "mobile development",

    # English - Other
    "blockchain", "solidity", "sap", "salesforce", "jira", "confluence",

    # Indonesian equivalents
    "pembelajaran mesin", "analisis data", "visualisasi data",
    "pengembangan perangkat lunak", "basis data", "jaringan komputer",
    "keamanan siber", "kecerdasan buatan", "pemrosesan bahasa alami",
    "pengembangan web", "pengembangan seluler", "manajemen proyek",
    "pemecahan masalah", "komunikasi", "kepemimpinan",
    "pengujian perangkat lunak", "arsitektur sistem",
]


def extract_skills(text: str) -> list:
    """Extract all skills from SKILL_LIST found in text (case-insensitive substring match)."""
    if not text or not text.strip():
        return []

    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        skill_lower = skill.lower()
        # Use word boundaries for single-letter or very short skills to avoid false positives
        if len(skill_lower) <= 2:
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill_lower)
        else:
            if skill_lower in text_lower:
                found_skills.append(skill_lower)

    return found_skills


def extract_education(text: str) -> str | None:
    """Extract highest education level from text based on priority order."""
    if not text or not text.strip():
        return None

    for pattern, label in _EDU_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return label

    return None


def extract_experience_years(text: str) -> int | None:
    """Extract largest mentioned years of experience from text."""
    if not text or not text.strip():
        return None

    matches = _EXP_PATTERN.findall(text)
    if not matches:
        return None

    return max(int(value) for value in matches)
