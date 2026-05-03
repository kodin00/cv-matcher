export interface Candidate {
  id: string;
  name: string;
  fileName: string;
  extractedText: string;
  status: 'processing' | 'completed' | 'error';
  errorMessage?: string;
  createdAt: Date;
}

export interface Job {
  id: string;
  title: string;
  company?: string;
  industry?: string;
  description: string;
  requirements: string[];
  requiredExperienceYears?: number | null;
  requiredEducation?: string | null;
  createdAt: Date;
}

export interface ScoreComparison {
  semantic_score: number;
  keyword_score: number;
  improvement: number;
}

export interface MatchBreakdown {
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
}

export interface MatchResult {
  jobId: string;
  jobTitle: string;
  candidateId: string;
  candidateName: string;
  grade: string;
  scoreComparison: ScoreComparison;
  breakdown: MatchBreakdown;
  processingTimeMs: number;
}

export interface ProcessingProgress {
  status: 'idle' | 'loading' | 'processing' | 'completed' | 'error';
  progress: number;
  message: string;
}
