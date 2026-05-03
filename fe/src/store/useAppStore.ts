import { create } from 'zustand';
import type { Candidate, Job, MatchResult } from '@/types';

interface AppState {
  candidates: Candidate[];
  selectedJob: Job | null;
  selectedJobId: string | null;
  matchResults: MatchResult[];
  isMatching: boolean;

  // Actions
  addCandidate: (candidate: Candidate) => void;
  updateCandidate: (id: string, updates: Partial<Candidate>) => void;
  removeCandidate: (id: string) => void;
  setSelectedJob: (job: Job | null) => void;
  setSelectedJobId: (id: string | null) => void;
  setMatchResults: (results: MatchResult[]) => void;
  setIsMatching: (isMatching: boolean) => void;
  clearAll: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  candidates: [],
  selectedJob: null,
  selectedJobId: null,
  matchResults: [],
  isMatching: false,

  addCandidate: (candidate) =>
    set(() => ({
      // Keep only 1 candidate at a time
      candidates: [candidate],
      matchResults: [],
    })),

  updateCandidate: (id, updates) =>
    set((state) => ({
      candidates: state.candidates.map((c) =>
        c.id === id ? { ...c, ...updates } : c
      ),
    })),

  removeCandidate: (id) =>
    set((state) => ({
      candidates: state.candidates.filter((c) => c.id !== id),
      matchResults: [],
    })),

  setSelectedJob: (job) =>
    set((state) => ({
      selectedJob: job,
      selectedJobId: job ? job.id : null,
      matchResults: state.selectedJobId !== job?.id ? [] : state.matchResults,
    })),

  setSelectedJobId: (id) =>
    set((state) => ({
      selectedJobId: id,
      matchResults: state.selectedJobId !== id ? [] : state.matchResults,
    })),

  setMatchResults: (results) =>
    set({
      matchResults: results,
    }),

  setIsMatching: (isMatching) =>
    set({
      isMatching,
    }),

  clearAll: () =>
    set({
      candidates: [],
      selectedJob: null,
      selectedJobId: null,
      matchResults: [],
      isMatching: false,
    }),
}));
