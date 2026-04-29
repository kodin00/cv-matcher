import { User, FileText, AlertCircle } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import type { Candidate } from '@/types';

interface CandidateDetailProps {
  candidate: Candidate | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CandidateDetail({
  candidate,
  open,
  onOpenChange,
}: CandidateDetailProps) {
  if (!candidate) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            {candidate.name}
          </DialogTitle>
        </DialogHeader>

        <div className="flex items-center gap-2 py-2">
          <Badge variant="outline">PDF</Badge>
          {candidate.status === 'completed' && (
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              <FileText className="h-3 w-3 mr-1" />
              Extraction Complete
            </Badge>
          )}
          {candidate.status === 'error' && (
            <Badge variant="destructive">
              <AlertCircle className="h-3 w-3 mr-1" />
              Processing Failed
            </Badge>
          )}
        </div>

        <ScrollArea className="flex-1 border rounded-lg p-4 bg-muted/30 max-h-96">
          {candidate.status === 'completed' && candidate.extractedText ? (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span>Extracted Text</span>
              </div>
              <pre className="text-sm whitespace-pre-wrap font-mono leading-relaxed">
                {candidate.extractedText}
              </pre>
            </div>
          ) : candidate.status === 'processing' ? (
            <div className="text-center py-8 text-muted-foreground">
              <p>Processing CV...</p>
            </div>
          ) : (
            <div className="text-center py-8 text-red-500">
              <p>{candidate.errorMessage || 'Failed to extract text'}</p>
            </div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
