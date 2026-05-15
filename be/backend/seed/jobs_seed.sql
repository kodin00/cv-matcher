-- Seed data: 30 Job Descriptions across 3 domains
-- 10 x Marketing (MK00001–MK00010)
-- 10 x Information Technology (IT00001–IT00010)
-- 10 x Finance (FN00001–FN00010)
-- Run: sqlite3 app.db < seed/jobs_seed.sql  (idempotent — INSERT OR IGNORE)

-- Remove the old two-job default dataset before applying the 30-job default set.
DELETE FROM jobs WHERE id IN ('jd-0001', 'jd-0002');

-- ============================================================
-- MARKETING
-- ============================================================

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00001',
    'Digital Marketing Specialist',
    'PT Tokopedia',
    'Marketing',
    'Digital Marketing Specialist akan bertanggung jawab atas perencanaan dan eksekusi kampanye digital marketing untuk berbagai vertical produk. Tugas utama: mengelola Google Ads dan Meta Ads dengan budget bulanan hingga IDR 500 juta, melakukan SEO on-page dan off-page optimization untuk meningkatkan organic traffic, menyusun content strategy untuk blog dan social media, melakukan A/B testing landing page, serta menganalisis performa kampanye menggunakan Google Analytics 4 dan Looker Studio. Kandidat ideal memiliki pengalaman minimum 2 tahun di digital marketing e-commerce atau marketplace, memiliki sertifikasi Google Ads dan Meta Blueprint, memahami funnel marketing (awareness, consideration, conversion, retention), serta menguasai tools seperti SEMrush, Ahrefs, atau Similarweb. Bilingual ID-EN untuk koordinasi dengan regional team.',
    '["SEO", "SEM", "Google Ads", "Meta Ads", "Google Analytics", "Content Marketing"]',
    2,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00002',
    'Brand Manager',
    'PT Unilever Indonesia',
    'Marketing',
    'Brand Manager untuk salah satu Personal Care brand portfolio kami. Tanggung jawab meliputi: mengembangkan brand strategy jangka panjang dan annual marketing plan, melakukan market research dan consumer insight untuk identifikasi growth opportunity, memimpin product innovation dan launch dari ideation sampai go-to-market, mengelola annual marketing budget dan ROI tracking, serta berkolaborasi dengan tim Trade Marketing dan Sales untuk eksekusi yang harmonis. Kandidat memiliki pengalaman minimum 5 tahun di brand management FMCG (preferably MNC), background pendidikan minimum S1 dari universitas top, fluent English untuk komunikasi dengan global team, memiliki strong analytical skill dengan exposure terhadap Nielsen retail audit dan Kantar Worldpanel data. Pengalaman product launch yang sukses akan menjadi keunggulan.',
    '["Brand Strategy", "Market Research", "Product Launch", "Consumer Insight", "Campaign Management"]',
    5,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00003',
    'Social Media Manager',
    'PT Paragon Technology and Innovation',
    'Marketing',
    'Social Media Manager akan memimpin strategi konten dan komunitas di seluruh platform sosial media Wardah (Instagram, TikTok, YouTube, Twitter). Lingkup pekerjaan: menyusun social media content calendar mingguan dan bulanan, mengelola komunitas online dan crisis management, memimpin influencer marketing program dengan KOL Tier 1-3, menganalisis performa konten dan engagement rate, serta mengkoordinasi tim copywriter dan content creator internal. Kandidat memiliki pengalaman 3-5 tahun di social media management khususnya brand beauty atau lifestyle, memahami platform algorithm masing-masing channel, memiliki portfolio konten yang strong, mahir Adobe Photoshop/Premiere atau CapCut, familiar dengan tools seperti Hootsuite, Sprout Social, atau Later. Pengalaman menangani crisis communication menjadi nilai tambah.',
    '["Social Media Strategy", "Content Creation", "Community Management", "Influencer Marketing", "Adobe Creative"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00004',
    'Performance Marketing Lead',
    'PT GoTo Gojek Tokopedia',
    'Marketing',
    'Performance Marketing Lead bertanggung jawab atas akuisisi user dan growth marketing untuk produk-produk GoPay. Tanggung jawab utama: memimpin strategy dan eksekusi paid acquisition channels (Google, Meta, TikTok, Apple Search Ads, programmatic), mengoptimalkan CAC, LTV, dan ROAS dengan budget bulanan multi-billion, mengembangkan attribution model menggunakan MMP seperti AppsFlyer atau Adjust, melakukan cohort analysis dan funnel optimization, serta memimpin tim 5-7 performance marketing specialists. Kandidat memiliki minimum 6 tahun pengalaman di performance marketing dengan minimum 2 tahun di leadership role, fluent dengan SQL dan BigQuery untuk data analysis, memahami advanced attribution (data-driven, MMM, incrementality testing), memiliki track record scaling app installs dan financial transactions. Latar belakang fintech atau e-commerce sangat diutamakan.',
    '["Performance Marketing", "Programmatic Ads", "Attribution Modeling", "MMP", "BigQuery", "SQL"]',
    6,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00005',
    'Content Marketing Strategist',
    'PT Kompas Gramedia',
    'Marketing',
    'Content Marketing Strategist akan memimpin pengembangan konten untuk berbagai brand di portfolio Kompas Gramedia. Lingkup pekerjaan: menyusun content strategy dan editorial calendar untuk blog korporat dan vertical-vertical bisnis, melakukan keyword research dan SEO content optimization, mengelola tim freelance writers dan content creators, melakukan content performance analysis (organic traffic, time on page, conversion), serta menjaga konsistensi brand voice dan tone of voice di seluruh kanal. Kandidat memiliki pengalaman 3-5 tahun di content marketing atau jurnalisme digital, memiliki portfolio tulisan yang kuat dalam Bahasa Indonesia maupun English, memahami SEO best practices (on-page, technical), familiar dengan WordPress, Yoast SEO, dan Surfer SEO. Latar belakang lulusan Komunikasi, Sastra, atau Jurnalistik diutamakan.',
    '["Content Strategy", "SEO Writing", "Editorial Calendar", "Storytelling", "WordPress"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00006',
    'Trade Marketing Executive',
    'PT Wings Group',
    'Marketing',
    'Trade Marketing Executive akan menjembatani fungsi Marketing dan Sales untuk eksekusi program di Modern Trade dan General Trade channel. Tanggung jawab: merancang dan eksekusi consumer promo dan trade promo program, memastikan ketersediaan POSM (Point of Sales Material) dan visual merchandising di outlet partner, melakukan store visit untuk monitor eksekusi dan competitor activity, menyusun program loyalty untuk modern trade key account, serta menganalisis sell-out data untuk evaluasi efektivitas program. Kandidat memiliki pengalaman 2-3 tahun di trade marketing FMCG, memahami dynamics modern trade (Indomaret, Alfamart, Hypermart) dan general trade, memiliki SIM A dan bersedia melakukan kunjungan ke outlet di area Jabodetabek, mahir Excel untuk sales analytics. Background distribusi atau sales operations menjadi nilai tambah.',
    '["Trade Marketing", "Visual Merchandising", "Channel Strategy", "Excel", "Sales Analytics"]',
    2,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00007',
    'Marketing Communications Manager',
    'PT Telkomsel',
    'Marketing',
    'Marketing Communications Manager bertanggung jawab atas seluruh aktivitas komunikasi pemasaran terintegrasi (IMC) di Telkomsel. Lingkup pekerjaan: menyusun integrated communication plan untuk product launches dan corporate campaigns, mengelola hubungan dengan media nasional dan agency partners (creative, media, PR), memimpin pelaksanaan corporate events dan brand activation, mengelola crisis communication dan reputation management, serta mengkoordinasi above-the-line dan below-the-line activities dengan internal stakeholders. Kandidat memiliki pengalaman minimum 5 tahun di marcomm atau PR (preferably agency atau MNC), memiliki networking kuat di kalangan media dan creative agency, fluent English dan memiliki kemampuan public speaking yang baik, memahami media planning dan budget management hingga miliaran rupiah.',
    '["Integrated Marketing Communication", "PR", "Event Management", "Media Relations", "Crisis Communication"]',
    5,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00008',
    'SEO Specialist',
    'PT Blibli.com',
    'Marketing',
    'SEO Specialist akan fokus pada peningkatan organic visibility website Blibli di search engine. Tanggung jawab utama: melakukan keyword research dan competitor analysis untuk berbagai kategori produk, technical SEO audit dan optimization (page speed, schema markup, internal linking), on-page SEO (title tag, meta description, content optimization), off-page SEO dan link building strategy, serta monitoring SERP performance dan organic traffic via Google Search Console dan Ahrefs. Kandidat memiliki pengalaman 2-3 tahun di SEO khususnya untuk website e-commerce dengan SKU besar, memahami Core Web Vitals dan Lighthouse audit, familiar dengan tools seperti Screaming Frog, Ahrefs, SEMrush, dan Google Search Console. Pemahaman dasar HTML/CSS dan JavaScript SEO menjadi nilai tambah penting.',
    '["SEO", "Technical SEO", "Keyword Research", "Link Building", "Screaming Frog", "Search Console"]',
    2,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00009',
    'Customer Experience Manager',
    'PT Allianz Life Indonesia',
    'Marketing',
    'Customer Experience Manager bertanggung jawab dalam mendesain dan meningkatkan customer journey end-to-end di Allianz Indonesia. Lingkup pekerjaan: melakukan customer journey mapping di seluruh touchpoint (digital dan offline), mengembangkan CX strategy untuk meningkatkan Net Promoter Score (NPS) dan Customer Satisfaction Index (CSI), berkolaborasi dengan tim Operations dan Product untuk implementasi pain point resolution, mengelola Voice of Customer program (VoC) melalui survey dan feedback channels, serta menggunakan data analytics untuk segmentation dan personalization. Kandidat memiliki pengalaman 5+ tahun di CX, customer insight, atau service design (preferably di financial services atau insurance), memahami CRM platform seperti Salesforce, mahir Tableau atau Power BI untuk visualization, memiliki sertifikasi CCXP atau Service Design menjadi nilai tambah.',
    '["CX Strategy", "NPS", "Customer Journey Mapping", "CRM", "Salesforce", "Tableau"]',
    5,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'MK00010',
    'Growth Marketing Analyst',
    'PT Ruangguru',
    'Marketing',
    'Growth Marketing Analyst akan menjadi bagian dari Growth team yang fokus pada akuisisi dan retention user platform Ruangguru. Tanggung jawab: melakukan analisis funnel marketing dari acquisition hingga conversion, menjalankan eksperimen A/B testing untuk landing page, email campaigns, dan in-app messaging, melakukan cohort analysis untuk memahami user retention pattern, mengembangkan growth model dan forecasting, serta menyusun growth dashboard menggunakan Mixpanel dan SQL queries. Kandidat memiliki pengalaman 2-3 tahun di growth marketing atau marketing analytics khususnya di startup atau tech company, mahir SQL untuk data analysis, familiar dengan product analytics tools (Mixpanel, Amplitude, atau GA4), memahami growth framework seperti AARRR (pirate metrics) dan ICE prioritization. Background statistik atau quantitative dari S1 favorable.',
    '["Growth Marketing", "Funnel Analysis", "A/B Testing", "SQL", "Mixpanel", "Cohort Analysis"]',
    2,
    'Bachelor'
);

-- ============================================================
-- INFORMATION TECHNOLOGY
-- ============================================================

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00001',
    'Backend Engineer',
    'PT Tokopedia',
    'Information Technology',
    'Backend Engineer akan bergabung dengan tim Marketplace Core Service untuk membangun dan memelihara API yang melayani jutaan transaksi harian. Tanggung jawab utama meliputi: mendesain dan mengimplementasikan microservices menggunakan Golang dengan arsitektur event-driven, mengoptimasi query PostgreSQL dan caching layer dengan Redis untuk handle high-traffic endpoint, melakukan code review dan unit testing, serta bekerja sama dengan tim DevOps untuk deployment ke Kubernetes cluster. Kandidat ideal memiliki pengalaman minimum 3 tahun di backend development dengan exposure ke production system bertraffic tinggi, menguasai konsep distributed system (CAP theorem, eventual consistency, message queue), familiar dengan observability stack (Prometheus, Grafana, ELK). Pengalaman dengan gRPC, Kafka, atau service mesh menjadi nilai tambah signifikan. Bilingual ID-EN untuk koordinasi dengan tim regional di Singapore.',
    '["Golang", "PostgreSQL", "Redis", "Kubernetes", "Microservices", "REST API"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00002',
    'Frontend Developer',
    'PT Bibit Tumbuh Bersama',
    'Information Technology',
    'Frontend Developer akan mengembangkan platform investasi yang digunakan oleh ratusan ribu retail investor Indonesia. Lingkup pekerjaan: membangun komponen UI yang reusable dan accessible (WCAG 2.1) menggunakan React dan TypeScript, mengimplementasikan halaman dengan Next.js dengan SSR/ISR untuk SEO performance, mengelola state aplikasi dengan Redux Toolkit, melakukan optimisasi performa (code splitting, lazy loading, bundle size reduction), dan kolaborasi erat dengan tim Product Designer untuk memastikan konsistensi design system. Kandidat memiliki pengalaman 2-4 tahun dengan modern frontend stack, paham konsep web performance (Core Web Vitals, Lighthouse), familiar dengan testing framework (Jest, React Testing Library, Cypress), pernah menangani aplikasi dengan scale lebih dari 100k DAU. Pengalaman di domain finansial atau keilmuan terkait fintech compliance menjadi keunggulan.',
    '["React", "TypeScript", "Next.js", "Tailwind CSS", "Redux", "Webpack"]',
    2,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00003',
    'DevOps Engineer',
    'PT Telkom Indonesia',
    'Information Technology',
    'DevOps Engineer Senior akan menjadi bagian dari Platform Engineering team yang mendukung infrastruktur produk-produk digital Telkom Group. Tanggung jawab utama: mengelola Kubernetes cluster di AWS EKS dengan ratusan microservices production, mengembangkan CI/CD pipeline dengan GitLab CI dan ArgoCD untuk GitOps deployment, menulis Infrastructure-as-Code menggunakan Terraform untuk provisioning resource AWS, mengimplementasikan monitoring dan alerting dengan Prometheus, Grafana, dan PagerDuty, serta memimpin incident response dan post-mortem analysis. Kandidat memiliki minimum 4 tahun pengalaman DevOps/SRE dengan exposure ke production cloud environment, menguasai Linux administration tingkat advanced, familiar dengan service mesh (Istio/Linkerd) dan secret management (Vault). Sertifikasi CKA, CKAD, atau AWS DevOps Professional sangat diutamakan. Bersedia on-call rotation.',
    '["Kubernetes", "Docker", "AWS", "Terraform", "GitLab CI", "Linux"]',
    4,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00004',
    'Mobile Developer (Android)',
    'PT Global Jet Express',
    'Information Technology',
    'Android Developer akan terlibat dalam pengembangan aplikasi kurir J&T yang digunakan oleh puluhan ribu driver harian di seluruh Indonesia. Tanggung jawab: mengembangkan fitur baru menggunakan Kotlin dan Jetpack Compose, memastikan arsitektur aplikasi mengikuti best practice MVVM dengan clean architecture, mengintegrasikan REST API dan handling offline-first scenario (kurir sering di area dengan sinyal lemah), menangani background task dengan WorkManager dan Coroutines, melakukan performance optimization (memory leak, ANR prevention, app startup time). Kandidat memiliki pengalaman 3-5 tahun di Android development, memiliki minimum 1 aplikasi yang sudah live di Play Store dengan rating lebih dari 4.0, paham Material Design 3 dan accessibility guidelines. Pengalaman dengan Maps SDK, push notification (FCM), dan analytics (Firebase, Mixpanel) sangat dibutuhkan.',
    '["Kotlin", "Jetpack Compose", "MVVM", "Coroutines", "Firebase", "REST API"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00005',
    'Data Engineer',
    'PT Gojek Indonesia',
    'Information Technology',
    'Data Engineer di tim Data Platform akan membangun dan memelihara data pipeline yang melayani analytics use case di seluruh business unit Gojek (Transport, Food, Pay, Ads). Tanggung jawab: mendesain ETL/ELT pipeline menggunakan Apache Airflow dengan ratusan DAG production, mengelola data warehouse di BigQuery dengan optimasi cost dan performance (partitioning, clustering, materialized view), implementasi data modeling dengan dbt mengikuti dimensional modeling, memproses streaming data dengan Apache Beam atau Spark Streaming, dan memastikan data quality melalui automated testing dan monitoring. Kandidat memiliki minimum 3 tahun pengalaman data engineering, mahir Python dan SQL tingkat advanced, familiar dengan modern data stack (Airflow, dbt, Looker), memahami konsep CDC (Change Data Capture) dan event-driven architecture. Pengalaman menangani data PII dengan compliance UU PDP menjadi keunggulan.',
    '["Python", "Apache Airflow", "BigQuery", "dbt", "Spark", "SQL"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00006',
    'QA Automation Engineer',
    'PT Ruangguru',
    'Information Technology',
    'QA Automation Engineer bertanggung jawab memastikan kualitas produk Ruangguru yang melayani jutaan siswa di Indonesia. Lingkup pekerjaan: merancang test strategy dan test plan untuk fitur baru, mengembangkan automated test suite untuk web (Cypress) dan API (Postman/RestAssured), mengintegrasikan automated test ke CI/CD pipeline dengan Jenkins, melakukan exploratory testing dan bug investigation, serta berkolaborasi dengan developer untuk implement TDD/BDD practice. Kandidat memiliki pengalaman 2-4 tahun di QA automation, memahami testing pyramid (unit, integration, e2e) dan kapan menggunakan masing-masing, familiar dengan Agile/Scrum methodology, memiliki pemikiran kritis untuk identify edge case yang luput dari requirement. Sertifikasi ISTQB Foundation menjadi nilai tambah.',
    '["Selenium", "Cypress", "Java", "TestNG", "Postman", "Jenkins"]',
    2,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00007',
    'Cybersecurity Analyst',
    'PT Bank Central Asia',
    'Information Technology',
    'Cybersecurity Analyst akan bergabung dengan Security Operations Center (SOC) BCA yang memantau keamanan sistem perbankan 24/7. Tanggung jawab utama: melakukan monitoring real-time dengan SIEM platform (Splunk/QRadar), menganalisis security event dan triage alert untuk identifikasi true positive, melakukan threat hunting proaktif menggunakan IoC dan TTP terbaru, memimpin incident response saat terjadi security breach mengikuti playbook NIST, dan melakukan vulnerability assessment serta penetration testing pada aplikasi internal. Kandidat memiliki minimum 3 tahun pengalaman di cybersecurity (SOC analyst, vulnerability assessment, atau red team), memahami framework ISO 27001 dan POJK 11/2022 tentang ketahanan dan keamanan siber bagi bank umum, familiar dengan tools seperti Burp Suite, Nmap, Metasploit, Wireshark. Sertifikasi CEH, OSCP, atau CompTIA Security+ sangat diutamakan.',
    '["SIEM", "Splunk", "Penetration Testing", "ISO 27001", "Network Security", "Incident Response"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00008',
    'UI/UX Designer',
    'PT Mekari',
    'Information Technology',
    'UI/UX Designer akan terlibat dalam pengembangan produk Mekari Talenta dan Mekari Jurnal yang digunakan oleh ribuan UKM dan korporasi di Indonesia. Tanggung jawab: melakukan user research (interview, usability testing, survey) untuk identify pain point pengguna, membuat user flow, wireframe, hingga high-fidelity prototype menggunakan Figma, berkolaborasi dengan Product Manager dan Engineer dalam discovery dan delivery phase, mengembangkan dan memelihara design system yang scalable, dan melakukan design review serta handoff yang detail untuk implementation. Kandidat memiliki pengalaman 3-5 tahun di product design (preferably B2B SaaS), memiliki portfolio yang menunjukkan end-to-end design process bukan hanya visual mockup, memahami konsep accessibility (WCAG) dan inclusive design, familiar dengan design ops practice. Pengalaman menangani complex enterprise software (HRIS, accounting, ERP) menjadi keunggulan utama.',
    '["Figma", "User Research", "Prototyping", "Design System", "Wireframing", "Usability Testing"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00009',
    'IT Support Specialist',
    'PT Astra Honda Motor',
    'Information Technology',
    'IT Support Specialist akan menjadi first point of contact untuk seluruh permasalahan IT karyawan di kantor pusat dan plant AHM. Lingkup pekerjaan: menangani helpdesk ticket terkait laptop, printer, jaringan, dan aplikasi internal (SAP, Microsoft 365), melakukan user provisioning dan deprovisioning di Active Directory, troubleshooting konektivitas LAN/WiFi dan VPN, instalasi serta maintenance hardware (PC, laptop, peripheral), serta dokumentasi knowledge base untuk recurring issue. Kandidat memiliki pengalaman 1-3 tahun di IT support atau helpdesk, lulusan D3/S1 IT atau setara, memahami konsep dasar networking (TCP/IP, DNS, DHCP, VPN), memiliki kemampuan komunikasi yang baik dan sabar dalam menghadapi end-user dari berbagai tingkat literasi digital. Sertifikasi CompTIA A+ atau ITIL Foundation menjadi nilai tambah. Bersedia ditempatkan rotasi antara HQ Jakarta dan plant Karawang sesuai kebutuhan.',
    '["Active Directory", "Windows Server", "Helpdesk", "Networking", "Hardware Troubleshooting"]',
    1,
    'Diploma'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'IT00010',
    'Product Manager (Tech)',
    'PT GoTo Gojek Tokopedia',
    'Information Technology',
    'Senior Product Manager akan memimpin product line di vertical Payment dan Lending GoPay. Tanggung jawab utama: mendefinisikan product vision, strategy, dan roadmap selaras dengan business OKR, memimpin discovery process dengan user research dan data analysis untuk identify problem yang worth solving, menulis Product Requirement Document (PRD) yang detail dan actionable untuk tim engineering, mengelola product backlog dan sprint planning bersama Engineering Lead dan Designer, melakukan A/B testing dan feature flagging untuk validate hypothesis, serta berkomunikasi dengan stakeholder lintas fungsi (Marketing, Risk, Compliance, Customer Service). Kandidat memiliki minimum 5 tahun pengalaman product management dengan minimum 2 tahun di fintech atau financial services, memahami unit economics dan growth metrics (CAC, LTV, retention), mahir SQL untuk self-service analytics, fluent English untuk komunikasi dengan investor dan partner internasional. Background engineering atau quantitative menjadi keunggulan untuk role technical PM ini.',
    '["Product Strategy", "Agile", "Roadmap", "Stakeholder Management", "SQL", "A/B Testing"]',
    5,
    'Bachelor'
);

-- ============================================================
-- FINANCE
-- ============================================================

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00001',
    'Financial Analyst',
    'PT Bank Mandiri',
    'Finance',
    'Kami mencari Financial Analyst yang berpengalaman untuk bergabung dengan tim Corporate Finance. Tanggung jawab utama meliputi: melakukan analisis kelayakan investasi (feasibility study), menyusun financial modeling untuk proyek korporasi, melakukan valuation perusahaan target akuisisi menggunakan metode DCF dan comparable company analysis, serta menyiapkan laporan keuangan bulanan kepada manajemen. Kandidat ideal memiliki pengalaman minimum 3 tahun di bidang corporate banking atau investment banking, menguasai financial modeling dengan Excel tingkat advanced, memahami standar IFRS dan PSAK, serta familiar dengan Bloomberg Terminal. Sertifikasi CFA Level 1 atau Brevet A/B menjadi nilai tambah. Memiliki kemampuan komunikasi bilingual (Bahasa Indonesia dan English) untuk presentasi kepada stakeholder internasional.',
    '["Financial Modeling", "Excel", "SQL", "Power BI", "Bloomberg Terminal", "IFRS"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00002',
    'Senior Risk Management Officer',
    'PT Bank Negara Indonesia',
    'Finance',
    'Bertanggung jawab dalam mengelola enterprise risk management framework di tingkat korporasi. Tugas utama mencakup pengembangan dan validasi credit risk model menggunakan PD (Probability of Default), LGD (Loss Given Default), dan EAD (Exposure at Default). Kandidat akan bekerja sama dengan tim Treasury dalam stress testing portfolio, monitoring kepatuhan terhadap regulasi OJK dan Basel III, serta menyusun Risk Appetite Statement. Pengalaman minimum 5 tahun di bidang risk management perbankan, menguasai metodologi quantitative risk modeling, mahir menggunakan SAS atau Python untuk analisis data risiko. Memiliki sertifikasi FRM atau ERMCP menjadi keunggulan. Pemahaman mendalam terhadap regulasi POJK terkait manajemen risiko bank umum sangat dibutuhkan.',
    '["Risk Assessment", "Basel III", "Credit Risk Modeling", "SAS", "Python", "OJK Regulation"]',
    5,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00003',
    'Investment Banking Associate',
    'PT Mandiri Sekuritas',
    'Finance',
    'Posisi Investment Banking Associate untuk Capital Markets Division. Akan terlibat dalam transaksi IPO, rights issue, obligasi korporasi, dan merger dan acquisition advisory. Tanggung jawab meliputi: penyusunan pitch book dan information memorandum, melakukan valuation menggunakan DCF, trading multiples, dan precedent transactions, membantu due diligence proses untuk transaksi M&A, serta berkomunikasi dengan klien korporasi dan regulator (OJK, BEI). Kualifikasi: minimum S2 Finance/Accounting/Economics dari universitas top, pengalaman 4-7 tahun di investment banking atau Big 4 transaction services, fluent in English (TOEFL 580+ atau IELTS 6.5+), menguasai financial modeling dan presentation skill. CFA Charterholder sangat diutamakan.',
    '["M&A", "DCF Valuation", "Pitch Book", "Excel", "PowerPoint", "Capital Markets"]',
    4,
    'Master'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00004',
    'Akuntan Pajak Senior',
    'KAP Mulyamin Sensi Suryanto',
    'Finance',
    'Senior Tax Consultant yang akan menangani klien korporasi dari berbagai industri. Tugas utama meliputi: penyusunan SPT Tahunan PPh Badan, perencanaan pajak (tax planning) yang sesuai dengan ketentuan UU Cipta Kerja, pendampingan pemeriksaan pajak (tax audit), penyusunan Transfer Pricing Documentation, serta melakukan tax review atas laporan keuangan klien. Kandidat harus memiliki sertifikasi Brevet A dan B (Brevet C menjadi nilai tambah), pengalaman minimum 4 tahun di Kantor Akuntan Publik atau Tax Consulting Firm, memahami PSAK dan IFRS, serta familiar dengan e-Faktur, e-SPT, dan DJP Online. Kemampuan komunikasi yang baik dalam Bahasa Indonesia dan English untuk klien multinasional.',
    '["Perpajakan", "Brevet AB", "e-Faktur", "e-SPT", "Accounting Software", "IFRS"]',
    4,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00005',
    'Treasury Manager',
    'PT Bank Rakyat Indonesia',
    'Finance',
    'Posisi Treasury Manager bertanggung jawab dalam pengelolaan likuiditas dan portofolio investasi bank. Lingkup pekerjaan: melakukan cash flow forecasting harian dan bulanan, mengelola posisi forex dan money market, melakukan ALM (Asset Liability Management) untuk menjaga NIM (Net Interest Margin), serta memastikan compliance terhadap regulasi GWM dan LCR. Kandidat ideal memiliki minimal 6 tahun pengalaman di Treasury department perbankan, menguasai instrumen pasar uang dan pasar modal, fluent dalam menggunakan Reuters/Bloomberg untuk dealing, serta memahami regulasi BI dan OJK terkait treasury. Sertifikasi ACI Dealing Certificate atau CTP menjadi nilai tambah.',
    '["Cash Management", "FX Trading", "Liquidity Management", "Treasury Management System", "Reuters"]',
    6,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00006',
    'Junior Auditor',
    'PT Deloitte Indonesia',
    'Finance',
    'Sebagai Junior Auditor, Anda akan menjadi bagian dari tim assurance yang melayani klien-klien Big Cap Indonesia di sektor perbankan, manufaktur, dan FMCG. Tugas utama: melakukan substantive testing dan test of control sesuai PSAK dan ISA, melakukan vouching dan tracing transaksi keuangan, menyusun Audit Working Papers, dan berkomunikasi dengan finance team klien. Persyaratan: fresh graduate atau pengalaman maksimum 2 tahun, lulusan S1 Akuntansi dari universitas terakreditasi A, IPK minimum 3.25, fluent in English (TOEFL min 500), memiliki sertifikasi CA atau Brevet AB menjadi keunggulan. Bersedia untuk lembur saat peak season dan dinas luar kota.',
    '["External Audit", "IFRS", "PSAK", "Excel", "Audit Software", "ISA"]',
    1,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00007',
    'Marketing Loan Officer',
    'PT Bank CIMB Niaga',
    'Finance',
    'Marketing Loan Officer bertanggung jawab dalam akuisisi nasabah kredit UMKM dan Komersial. Tanggung jawab utama: melakukan customer prospecting dan business development di area Tangerang dan sekitarnya, menganalisis kelayakan kredit calon debitur (5C analysis - character, capacity, capital, collateral, condition), melakukan KYC dan customer due diligence sesuai regulasi APU-PPT, serta mencapai target portfolio kredit bulanan. Kandidat memiliki pengalaman minimum 2 tahun di sales perbankan atau lembaga keuangan, memahami produk kredit modal kerja dan investasi, memiliki SIM A dan kendaraan pribadi, serta memiliki networking yang kuat di komunitas pengusaha lokal. Kemampuan negosiasi dan komunikasi yang baik adalah mutlak.',
    '["Credit Analysis", "Customer Acquisition", "KYC", "Loan Processing", "Sales"]',
    2,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00008',
    'Compliance Officer',
    'PT Bank Danamon Indonesia',
    'Finance',
    'Compliance Officer bertugas memastikan seluruh aktivitas operasional bank mematuhi regulasi yang berlaku. Tanggung jawab utama meliputi: monitoring transaksi nasabah untuk mendeteksi suspicious transaction (STR/CTR), melakukan compliance review terhadap produk dan layanan baru, menjadi liaison officer dengan PPATK dan OJK, serta menyusun laporan kepatuhan bulanan. Kandidat ideal memiliki pengalaman minimum 4 tahun di compliance, audit internal, atau risk management, menguasai regulasi APU-PPT, FATCA, dan POJK terkait perbankan, memiliki sertifikasi ACAMS atau CAMS menjadi nilai tambah signifikan. Fluent English untuk komunikasi dengan principal di Malaysia.',
    '["AML", "KYC", "Compliance Monitoring", "OJK Regulation", "FATCA", "Internal Audit"]',
    4,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00009',
    'Financial Planning Analyst',
    'PT Astra International',
    'Finance',
    'Financial Planning & Analysis Analyst akan bergabung dengan Corporate Finance team. Lingkup pekerjaan: menyusun annual budget dan rolling forecast untuk seluruh business unit, melakukan variance analysis (actual vs budget vs forecast), menyiapkan Monthly Business Review (MBR) untuk Board of Directors, serta mendukung CapEx evaluation dan post-investment review. Kandidat memiliki pengalaman 3-5 tahun di FP&A atau Management Accounting, menguasai SAP BPC atau Hyperion, mahir Excel advanced (Power Query, Power Pivot), memahami consolidated financial statements untuk grup perusahaan multi-entitas. Memiliki latar belakang Big 4 audit atau perusahaan multinasional menjadi nilai tambah. Sertifikasi CMA atau CPA diutamakan.',
    '["FP&A", "Budgeting", "Forecasting", "SAP BPC", "Excel", "Power BI"]',
    3,
    'Bachelor'
);

INSERT OR IGNORE INTO jobs (id, title, company, industry, description, required_skills, required_experience_years, required_education) VALUES (
    'FN00010',
    'Branch Manager',
    'PT Bank Mega',
    'Finance',
    'Branch Manager bertanggung jawab atas keseluruhan operasional cabang termasuk pencapaian target bisnis, kualitas layanan nasabah, dan kepatuhan operasional. Tanggung jawab utama: memimpin tim 15-25 staff cabang termasuk Customer Service, Teller, dan Marketing, mencapai target funding dan lending yang ditetapkan kantor pusat, menjaga service quality index dan customer satisfaction score, serta memastikan compliance terhadap SOP dan regulasi. Kandidat memiliki minimum 7 tahun pengalaman di banking dengan minimal 2 tahun sebagai Assistant Branch Manager atau setara, menguasai produk perbankan retail dan UKM, memiliki kemampuan leadership dan people management yang kuat, serta familiar dengan target-driven environment. Memiliki networking yang luas di area Bekasi dan sekitarnya.',
    '["Branch Operations", "Team Leadership", "Sales Management", "Customer Service", "Banking Products"]',
    7,
    'Bachelor'
);
