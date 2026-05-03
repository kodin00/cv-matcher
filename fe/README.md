# CV Matcher - Candidate Filtering System

A clean, modern frontend for a CV-to-job matching system. Compare a single CV against a single job description and get both semantic and keyword match scores.

## Features

- **PDF Text Extraction**: Processes PDFs using PDF.js direct text extraction (no OCR)
- **Drag & Drop Upload**: Easy file upload with progress tracking
- **Job Management**: Add a single job description for comparison
- **Dual Matching Results**: See both semantic match % and keyword match % side by side
- **Clean UI**: Modern, minimal interface built with React + Tailwind CSS

## Tech Stack

- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui components
- PDF.js (PDF text extraction)
- Zustand (state management)

## Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Docker

```bash
# From the repository root, build and run frontend + backend together
make docker

# Or use Docker Compose directly
docker compose -f docker-compose.yml up --build
```

The app will be available at `http://localhost:4000`

## Project Structure

```
src/
  components/
    ui/                  # shadcn/ui components
    FileUpload.tsx       # CV upload (PDF only)
    JobManager.tsx       # Job description management
    MatchButton.tsx      # Trigger matching
    MatchResults.tsx     # Display dual match scores
    CandidateDetail.tsx  # View extracted CV text
  store/
    useAppStore.ts       # Zustand state management
  types/
    index.ts             # TypeScript types
  utils/
    cn.ts                # Tailwind class merging
    pdfExtractor.ts      # PDF text extraction logic
    matcher.ts           # Keyword + semantic scoring algorithms
```

## PDF Extraction

- Supports PDF files only
- Extracts text directly from PDF using PDF.js (no OCR needed)
- Processes first 5 pages of PDFs (optimized for CVs)

## Backend Integration

The frontend calls the Flask backend endpoints directly:

- `GET /api/jobs`
- `GET /api/jobs/:jobId`
- `POST /api/match`

In local dev, `make dev` passes the backend token from `be/backend/.env` into Vite. In Docker, nginx serves the frontend and proxies `/api/*` to the backend service while adding the backend token server-side.

The backend returns both semantic and keyword scores for comparison.

## Environment Variables

Create `.env` file for configuration:

```
VITE_API_URL=http://localhost:5000
VITE_API_TOKEN=<same value as APP_TOKEN in ../be/backend/.env>
```

## Building for Production

```bash
npm run build
```

Output will be in `dist/` directory.

## License

MIT
