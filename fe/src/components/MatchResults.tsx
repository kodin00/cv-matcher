import { useState } from 'react';
import { Trophy, User, Building2, Sparkles, Hash, GraduationCap, Briefcase, Clock } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { CandidateDetail } from './CandidateDetail';
import { useAppStore } from '@/store/useAppStore';
import type { Candidate } from '@/types';

interface MatchResultsProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

function getGradeColor(grade: string): string {
  switch (grade) {
    case 'High Match':
      return 'bg-green-100 text-green-800 border-green-300';
    case 'Medium Match':
      return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    case 'Low Match':
      return 'bg-red-100 text-red-800 border-red-300';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-300';
  }
}

export function MatchResults({ open, onOpenChange }: MatchResultsProps) {
  const { candidates, selectedJob, matchResults } = useAppStore();
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);

  const result = matchResults[0];
  const candidate = candidates.find((c) => c.id === result?.candidateId);

  const handleViewCandidate = (candidate: Candidate) => {
    setSelectedCandidate(candidate);
    setDetailOpen(true);
  };

  if (!selectedJob || !result || !candidate) return null;

  const { scoreComparison, breakdown, grade } = result;

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="max-w-xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Trophy className="h-5 w-5 text-yellow-500" />
              Matching Results
            </DialogTitle>
          </DialogHeader>

          <div className="space-y-4 mt-4">
            {/* Grade Badge */}
            <div className="flex justify-center">
              <Badge
                variant="outline"
                className={`text-lg px-4 py-1 ${getGradeColor(grade)}`}
              >
                {grade}
              </Badge>
            </div>

            {/* Selected Job Header */}
            <Card className="bg-muted/50">
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <Building2 className="h-5 w-5 text-primary" />
                  <div>
                    <h3 className="font-semibold">{selectedJob.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {selectedJob.company}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Candidate Info */}
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-4">
                  <User className="h-4 w-4 text-muted-foreground" />
                  <span className="font-medium">{candidate.name}</span>
                </div>

                {/* Two Scores Side by Side */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  {/* Semantic Match */}
                  <div className="rounded-lg bg-primary/5 p-4 text-center">
                    <div className="flex items-center justify-center gap-1.5 text-sm text-muted-foreground mb-1">
                      <Sparkles className="h-4 w-4 text-primary" />
                      Semantic Match
                    </div>
                    <div className="text-3xl font-bold text-primary">
                      {scoreComparison.semantic_score}%
                    </div>
                  </div>

                  {/* Keyword Match */}
                  <div className="rounded-lg bg-secondary/50 p-4 text-center">
                    <div className="flex items-center justify-center gap-1.5 text-sm text-muted-foreground mb-1">
                      <Hash className="h-4 w-4 text-secondary-foreground" />
                      Keyword Match
                    </div>
                    <div className="text-3xl font-bold text-secondary-foreground">
                      {scoreComparison.keyword_score}%
                    </div>
                  </div>
                </div>

                {/* Improvement Note */}
                <p className="text-xs text-muted-foreground text-center mb-4">
                  Improvement: {scoreComparison.improvement > 0 ? '+' : ''}
                  {scoreComparison.improvement} points over keyword baseline
                </p>

                {/* Skills Breakdown */}
                <div className="space-y-3 border-t pt-4">
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-primary" />
                    <h4 className="text-sm font-medium">Skills Analysis</h4>
                    <span className="text-xs text-muted-foreground ml-auto">
                      Score: {breakdown.skills.score}% (weight: {breakdown.skills.weight * 100}%)
                    </span>
                  </div>
                  <Progress value={breakdown.skills.score} className="h-2" />

                  {breakdown.skills.matched_skills.length > 0 && (
                    <div>
                      <p className="text-xs text-green-600 font-medium mb-1.5">Matched Skills</p>
                      <div className="flex flex-wrap gap-1.5">
                        {breakdown.skills.matched_skills.map((skill, i) => (
                          <Badge key={i} variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {breakdown.skills.missing_skills.length > 0 && (
                    <div>
                      <p className="text-xs text-red-600 font-medium mb-1.5">Missing Skills</p>
                      <div className="flex flex-wrap gap-1.5">
                        {breakdown.skills.missing_skills.map((skill, i) => (
                          <Badge key={i} variant="outline" className="text-xs bg-red-50 text-red-700 border-red-200">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Experience Breakdown */}
                <div className="space-y-2 border-t pt-4">
                  <div className="flex items-center gap-2">
                    <Briefcase className="h-4 w-4 text-primary" />
                    <h4 className="text-sm font-medium">Experience</h4>
                    <span className="text-xs text-muted-foreground ml-auto">
                      Score: {breakdown.experience.score}% (weight: {breakdown.experience.weight * 100}%)
                    </span>
                  </div>
                  <Progress value={breakdown.experience.score} className="h-2" />
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Detected: {breakdown.experience.years_detected ?? 'N/A'} years</span>
                    <span>Required: {breakdown.experience.years_required ?? 'N/A'} years</span>
                  </div>
                </div>

                {/* Education Breakdown */}
                <div className="space-y-2 border-t pt-4">
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-4 w-4 text-primary" />
                    <h4 className="text-sm font-medium">Education</h4>
                    <span className="text-xs text-muted-foreground ml-auto">
                      Score: {breakdown.education.score}% (weight: {breakdown.education.weight * 100}%)
                    </span>
                  </div>
                  <Progress value={breakdown.education.score} className="h-2" />
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Detected: {breakdown.education.detected ?? 'N/A'}</span>
                    <span>Required: {breakdown.education.required ?? 'N/A'}</span>
                  </div>
                </div>

                {/* Processing Time */}
                <div className="flex items-center gap-1.5 text-xs text-muted-foreground border-t pt-3">
                  <Clock className="h-3 w-3" />
                  Processed in {result.processingTimeMs}ms
                </div>

                <div className="mt-4 flex justify-end">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleViewCandidate(candidate)}
                  >
                    View CV
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </DialogContent>
      </Dialog>

      <CandidateDetail
        candidate={selectedCandidate}
        open={detailOpen}
        onOpenChange={setDetailOpen}
      />
    </>
  );
}
