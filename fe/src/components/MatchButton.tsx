import { useState } from 'react';
import { Play, Loader2, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAppStore } from '@/store/useAppStore';
import { matchCv } from '@/api/client';
import type { MatchResult } from '@/types';

interface MatchButtonProps {
  onMatchComplete?: () => void;
}

export function MatchButton({ onMatchComplete }: MatchButtonProps) {
  const { candidates, selectedJob, setMatchResults, setIsMatching, isMatching } =
    useAppStore();
  const [showSuccess, setShowSuccess] = useState(false);

  const candidate = candidates.find((c) => c.status === 'completed');
  const canMatch = !!candidate && !!selectedJob;

  const handleMatch = async () => {
    if (!canMatch || !candidate || !selectedJob) return;

    setIsMatching(true);
    setShowSuccess(false);

    try {
      const response = await matchCv({
        job_id: selectedJob.id,
        candidate_id: candidate.id,
        candidate_name: candidate.name,
        cv_text: candidate.extractedText,
      });

      const result: MatchResult = {
        jobId: response.job_id,
        jobTitle: response.job_title,
        candidateId: response.candidate_id,
        candidateName: response.candidate_name,
        grade: response.grade,
        scoreComparison: response.score_comparison,
        breakdown: response.breakdown,
        processingTimeMs: response.processing_time_ms,
      };

      setMatchResults([result]);
      setShowSuccess(true);
      onMatchComplete?.();
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Matching failed';
      alert(message);
    } finally {
      setIsMatching(false);
    }
  };

  return (
    <Button
      size="default"
      disabled={!canMatch || isMatching}
      onClick={handleMatch}
    >
      {isMatching ? (
        <>
          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
          Matching...
        </>
      ) : showSuccess ? (
        <>
          <CheckCircle2 className="h-4 w-4 mr-2" />
          Matching Complete
        </>
      ) : (
        <>
          <Play className="h-4 w-4 mr-2" />
          Match CV to Job
        </>
      )}
    </Button>
  );
}
