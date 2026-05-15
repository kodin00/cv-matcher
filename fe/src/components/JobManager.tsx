import { useState, useEffect } from 'react';
import { Building2, Loader2, AlertCircle, CheckCircle2, ChevronLeft, ChevronRight } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useAppStore } from '@/store/useAppStore';
import { fetchJobs, fetchJob, type JobListItem, type JobDetail } from '@/api/client';
import { Job } from '@/types';

const JOBS_PER_PAGE = 10;

export function JobManager() {
  const { selectedJob, setSelectedJob } = useAppStore();
  const [jobs, setJobs] = useState<JobListItem[]>([]);
  const [page, setPage] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selectingJobId, setSelectingJobId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchJobs(page, JOBS_PER_PAGE)
      .then((data) => {
        setJobs(data.jobs);
        setTotalJobs(data.total);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Failed to load jobs');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [page]);

  const totalPages = Math.max(1, Math.ceil(totalJobs / JOBS_PER_PAGE));
  const firstJobNumber = totalJobs === 0 ? 0 : (page - 1) * JOBS_PER_PAGE + 1;
  const lastJobNumber = Math.min(page * JOBS_PER_PAGE, totalJobs);

  const handleSelectJob = async (jobItem: JobListItem) => {
    if (selectedJob?.id === jobItem.job_id) return;

    try {
      setSelectingJobId(jobItem.job_id);
      setError(null);
      const detail: JobDetail = await fetchJob(jobItem.job_id);
      const job: Job = {
        id: detail.job_id,
        title: detail.title,
        company: detail.company,
        industry: detail.industry,
        description: detail.description,
        requirements: detail.required_skills || [],
        requiredExperienceYears: detail.required_experience_years,
        requiredEducation: detail.required_education,
        createdAt: new Date(detail.created_at),
      };
      setSelectedJob(job);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load job details');
    } finally {
      setSelectingJobId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-8 text-muted-foreground">
        <Loader2 className="h-5 w-5 mr-2 animate-spin" />
        Loading jobs...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-start gap-2 py-4 text-red-500">
        <AlertCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-medium">Failed to load jobs</p>
          <p className="text-sm">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
            Select a job from the list below
          </p>
          {totalJobs > JOBS_PER_PAGE && (
            <p className="mt-1 text-xs text-muted-foreground">
              Showing {firstJobNumber}-{lastJobNumber} of {totalJobs}
            </p>
          )}
        </div>

        {totalJobs > JOBS_PER_PAGE && (
          <div className="flex items-center gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setPage((currentPage) => Math.max(1, currentPage - 1))}
              disabled={page === 1 || loading}
            >
              <ChevronLeft className="mr-1 h-4 w-4" />
              Prev
            </Button>
            <span className="text-xs text-muted-foreground">
              Page {page} of {totalPages}
            </span>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setPage((currentPage) => Math.min(totalPages, currentPage + 1))}
              disabled={page === totalPages || loading}
            >
              Next
              <ChevronRight className="ml-1 h-4 w-4" />
            </Button>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 gap-2">
        {jobs.map((job) => {
          const isSelected = selectedJob?.id === job.job_id;
          const isSelecting = selectingJobId === job.job_id;

          return (
            <Card
              key={job.job_id}
              className={`cursor-pointer transition-all ${
                isSelected
                  ? 'border-2 border-primary ring-1 ring-primary'
                  : 'border-dashed hover:border-primary hover:ring-1 hover:ring-primary'
              }`}
              onClick={() => handleSelectJob(job)}
            >
              <CardContent className="p-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <Building2
                        className={`h-4 w-4 flex-shrink-0 ${
                          isSelected ? 'text-primary' : 'text-muted-foreground'
                        }`}
                      />
                      <h4 className="font-medium text-sm truncate">{job.title}</h4>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {job.company}
                      {job.industry && ` / ${job.industry}`}
                      {job.required_experience_years !== null && ` / ${job.required_experience_years}+ years`}
                    </p>
                  </div>

                  {isSelecting && (
                    <Loader2 className="h-4 w-4 flex-shrink-0 animate-spin text-primary" />
                  )}
                </div>

                {isSelected && selectedJob && (
                  <div className="mt-3 space-y-3 border-t pt-3">
                    {selectedJob.description && (
                      <p className="text-sm text-muted-foreground">
                        {selectedJob.description}
                      </p>
                    )}

                    {selectedJob.requirements.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {selectedJob.requirements.map((skill, i) => (
                          <Badge key={i} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    )}

                    <div className="grid gap-1 text-xs text-muted-foreground sm:grid-cols-2">
                      {(selectedJob.requiredExperienceYears !== null &&
                        selectedJob.requiredExperienceYears !== undefined) && (
                        <p>Experience: {selectedJob.requiredExperienceYears} years</p>
                      )}
                      {selectedJob.requiredEducation && (
                        <p>Education: {selectedJob.requiredEducation}</p>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {jobs.length === 0 && (
        <div className="text-center py-6 text-muted-foreground">
          <CheckCircle2 className="h-8 w-8 mx-auto mb-2 opacity-50" />
          <p className="text-sm">No jobs available</p>
          <p className="text-xs">Jobs will appear here once added to the backend.</p>
        </div>
      )}

    </div>
  );
}
