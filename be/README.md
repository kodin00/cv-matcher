# cv-processor

Backend REST API for a bilingual CV semantic matching system. Receives a pre-extracted CV text string from the frontend (OCR is handled on the FE side), matches it against a job posting using multilingual sentence embeddings, and returns the match result alongside a TF-IDF keyword baseline score for direct comparison.

> **Skripsi:** Perancangan Sistem Filtering Kandidat Berdasarkan Kualifikasi Menggunakan Analisis Semantik Berbasis Machine Learning pada Data Curriculum Vitae

---

## Tech Stack

| Layer | Library / Tool | Purpose |
|---|---|---|
| Web Framework | `Flask` | REST API server |
| Auth | Static UUID token in `.env` | Simple Bearer token auth |
| NLP Preprocessing | `langdetect`, `re`, `unicodedata` | Text cleaning, language detection |
| Skill Extraction | `spaCy` + custom bilingual skill list | Rule-based NER for skills |
| Embedding Model | `sentence-transformers` (`paraphrase-multilingual-mpnet-base-v2`) | Cross-lingual sentence embeddings |
| Similarity | `scikit-learn` (`cosine_similarity`) | Compute semantic match scores |
| Baseline | `scikit-learn` (`TfidfVectorizer`) | TF-IDF keyword matching — always returned alongside semantic score |
| Data Store | `SQLite` (via `SQLAlchemy`) | Job descriptions — read-only from API |
| Env/Config | `python-dotenv` | Token & config management |
| CORS | `flask-cors` | Allow cross-origin requests from the FE |

---

## Project Structure

```
backend/
├── app.py                      # Flask entry point
├── config.py                   # Env vars, token, model name
├── requirements.txt
├── seed/
│   ├── schema.sql              # Idempotent CREATE TABLE statement
│   └── jobs_seed.sql           # INSERT OR IGNORE seed data
│
├── middleware/
│   └── auth.py                 # Static Bearer token validation
│
├── routes/
│   ├── match.py                # POST /api/match
│   ├── jobs.py                 # GET /api/jobs, GET /api/jobs/<id>
│   └── health.py               # GET /api/health
│
├── services/
│   ├── preprocessing.py        # Text cleaning & normalization
│   ├── extraction.py           # Rule-based skill & section extraction
│   ├── embedding_service.py    # Sentence embeddings (loaded once at startup)
│   └── baseline_service.py     # TF-IDF keyword matching (paper baseline)
│
├── models/
│   └── db_models.py            # SQLAlchemy Job model
│
└── utils/
    └── response_utils.py       # Standardised JSON response helpers
```

---

## Setup

### 1. Create a virtual environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
python -m spacy download xx_ent_wiki_sm
```

> **Note:** If you encounter issues with CUDA dependencies during installation, you can install CPU-only PyTorch:
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```

### 3. Configure environment

```bash
cp backend/.env.example backend/.env
# Edit backend/.env — set APP_TOKEN to a real UUID
# Example: uuidgen | tr -d '\n' (Linux/macOS) to generate a UUID
```

### 4. Initialise the database

```bash
cd backend
sqlite3 app.db < seed/schema.sql
sqlite3 app.db < seed/jobs_seed.sql
```

### 5. Run

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Development (run from the backend/ directory — app uses relative imports)
cd backend
python app.py

# Production
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app
```

---

## Docker

```bash
cp backend/.env.example backend/.env
# Edit backend/.env — set APP_TOKEN to a real UUID
docker compose up --build
```

The entrypoint script automatically applies schema and seed data on first run. The SQLite database is stored on a named Docker volume and persists across container restarts.

Service available at: `http://localhost:5000/api/health`

### Docker deployment quickstart (VM)

```bash
# 1) Prepare runtime env file
cp backend/.env.example backend/.env

# 2) Set APP_TOKEN in backend/.env
uuidgen

# 3) Build and run
docker compose up --build -d

# 4) Verify health
curl -f http://localhost:5000/api/health
```

Optional verification:

```bash
# Confirm seeded jobs exist (requires APP_TOKEN from backend/.env)
TOKEN="<your-app-token>"
curl -s -H "Authorization: Bearer $TOKEN" \
    "http://localhost:5000/api/jobs?page=1&limit=10"

# Stop services but keep DB data
docker compose down

# Bring back up (data persists in named volume)
docker compose up -d

# Remove services + DB volume (data reset)
docker compose down -v
```

---

## API Endpoints

All endpoints except `/api/health` require: `Authorization: Bearer <token>`

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Liveness check — no auth required |
| `GET` | `/api/jobs` | List job postings (supports `industry`, `page`, `limit` query params) |
| `GET` | `/api/jobs/<job_id>` | Get full job detail |
| `POST` | `/api/match` | Single-candidate CV matching — returns semantic and keyword scores with breakdown |

### POST /api/match

Accepts a single candidate per request. Required fields: `job_id`, `candidate_id`, `candidate_name`, `cv_text` (pre-extracted plain text). Returns semantic and TF-IDF keyword scores side by side with a per-section breakdown.

**Grade thresholds** (based on `semantic_score`):

| Score | Grade |
|---|---|
| ≥ 80 | High Match |
| 60–79 | Medium Match |
| < 60 | Low Match |

---

## Scoring

`semantic_score = (skills_score × 0.4) + (experience_score × 0.4) + (education_score × 0.2)`

The `score_comparison` block in every result contains:
- `semantic_score` — weighted cosine similarity from multilingual sentence embeddings (0–100)
- `keyword_score` — TF-IDF bag-of-words cosine similarity score (0–100)
- `improvement` — `semantic_score − keyword_score` (quantifies the gain from semantic over keyword matching)
