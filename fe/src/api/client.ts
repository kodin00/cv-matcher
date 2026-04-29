const API_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
const API_TOKEN = import.meta.env.VITE_API_TOKEN || '';

function getHeaders(): Record<string, string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (API_TOKEN) {
    headers.Authorization = `Bearer ${API_TOKEN}`;
  }

  return headers;
}

function apiPath(path: string): string {
  return `${API_URL}${path}`;
}

async function handleResponse<T>(res: Response): Promise<T> {
  const data = await res.json().catch(() => ({
    status: 'error',
    message: `Request failed with status ${res.status}`,
  }));

  if (!res.ok) {
    throw new Error(data.message || `Request failed with status ${res.status}`);
  }

  if (data.status === 'error') {
    throw new Error(data.message || 'API error');
  }

  return data;
}

export interface JobListItem {
  job_id: string;
  title: string;
  company: string;
  industry: string;
  required_experience_years: number | null;
  created_at: string;
}

export interface JobDetail {
  job_id: string;
  title: string;
  company: string;
  industry: string;
  description: string;
  required_skills: string[];
  required_experience_years: number | null;
  required_education: string | null;
  created_at: string;
}

export interface JobsResponse {
  status: string;
  total: number;
  page: number;
  limit: number;
  jobs: JobListItem[];
}

export interface MatchRequest {
  job_id: string;
  candidate_id: string;
  candidate_name: string;
  cv_text: string;
}

export interface MatchResponse {
  status: string;
  job_id: string;
  job_title: string;
  candidate_id: string;
  candidate_name: string;
  language_detected: string;
  grade: string;
  score_comparison: {
    semantic_score: number;
    keyword_score: number;
    improvement: number;
  };
  breakdown: {
    skills: {
      score: number;
      weight: number;
      matched_skills: string[];
      missing_skills: string[];
    };
    experience: {
      score: number;
      weight: number;
      years_detected: number | null;
      years_required: number | null;
    };
    education: {
      score: number;
      weight: number;
      detected: string | null;
      required: string | null;
    };
  };
  processing_time_ms: number;
}

export async function fetchJobs(): Promise<JobListItem[]> {
  const res = await fetch(apiPath('/api/jobs'), {
    method: 'GET',
    headers: getHeaders(),
  });
  const data = await handleResponse<JobsResponse>(res);
  return data.jobs;
}

export async function fetchJob(jobId: string): Promise<JobDetail> {
  const res = await fetch(apiPath(`/api/jobs/${jobId}`), {
    method: 'GET',
    headers: getHeaders(),
  });
  return handleResponse<JobDetail>(res);
}

export async function matchCv(request: MatchRequest): Promise<MatchResponse> {
  const res = await fetch(apiPath('/api/match'), {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(request),
  });
  return handleResponse<MatchResponse>(res);
}
