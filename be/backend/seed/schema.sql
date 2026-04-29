CREATE TABLE IF NOT EXISTS jobs (
    id                        TEXT PRIMARY KEY,
    title                     TEXT NOT NULL,
    company                   TEXT NOT NULL,
    industry                  TEXT NOT NULL,
    description               TEXT NOT NULL,
    required_skills           TEXT NOT NULL,
    required_experience_years INTEGER,
    required_education        TEXT,
    created_at                TEXT DEFAULT (datetime('now'))
);
