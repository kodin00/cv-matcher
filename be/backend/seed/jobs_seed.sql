INSERT OR IGNORE INTO jobs (
    id,
    title,
    company,
    industry,
    description,
    required_skills,
    required_experience_years,
    required_education
)
VALUES (
    'jd-0001',
    'Software Engineer',
    'PT Teknologi Maju',
    'Information Technology',
    'Backend engineering role with REST API and SQL experience. Mampu bekerja kolaboratif dalam tim pengembangan perangkat lunak.',
    '["Python", "REST API", "SQL", "Git", "Docker"]',
    2,
    'S1 Ilmu Komputer / Bachelor of Computer Science'
);

INSERT OR IGNORE INTO jobs (
    id,
    title,
    company,
    industry,
    description,
    required_skills,
    required_experience_years,
    required_education
)
VALUES (
    'jd-0002',
    'Data Analyst',
    'PT Keuangan Nusantara',
    'Finance',
    'Responsible for analyzing financial datasets and building dashboards. Bertanggung jawab menganalisis data keuangan dan menyajikan laporan visual.',
    '["Python", "SQL", "Tableau", "Excel", "Statistics"]',
    1,
    'S1 Statistika / Matematika / Ilmu Komputer'
);
