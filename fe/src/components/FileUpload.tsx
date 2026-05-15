import { useState } from 'react';
import { Upload, FileText, X, Loader2, Eye, Briefcase } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { processFile } from '@/utils/pdfExtractor';
import { useAppStore } from '@/store/useAppStore';
import { generateUUID } from '@/utils/uuid';
import { Candidate, ProcessingProgress } from '@/types';

const EXAMPLE_CVS = [
  {
    id: 'mk-amelia',
    name: 'Amelia Putri',
    targetJob: 'MK00001 - Digital Marketing Specialist',
    fileName: 'cv_mk00001_amelia_putri_digital_marketing.pdf',
    path: '/example-cvs/cv_mk00001_amelia_putri_digital_marketing.pdf',
  },
  {
    id: 'mk-rizky',
    name: 'Rizky Nugroho',
    targetJob: 'MK00001 - Digital Marketing Specialist',
    fileName: 'cv_mk00001_rizky_nugroho_growth_marketer.pdf',
    path: '/example-cvs/cv_mk00001_rizky_nugroho_growth_marketer.pdf',
  },
  {
    id: 'mk-sari',
    name: 'Sari Wulandari',
    targetJob: 'MK00001 - Digital Marketing Specialist',
    fileName: 'cv_mk00001_sari_wulandari_high_match.pdf',
    path: '/example-cvs/cv_mk00001_sari_wulandari_high_match.pdf',
  },
  {
    id: 'it-bima',
    name: 'Bima Santoso',
    targetJob: 'IT00001 - Backend Engineer',
    fileName: 'cv_it00001_bima_santoso_backend_engineer.pdf',
    path: '/example-cvs/cv_it00001_bima_santoso_backend_engineer.pdf',
  },
  {
    id: 'it-nadia',
    name: 'Nadia Lestari',
    targetJob: 'IT00001 - Backend Engineer',
    fileName: 'cv_it00001_nadia_lestari_backend_platform.pdf',
    path: '/example-cvs/cv_it00001_nadia_lestari_backend_platform.pdf',
  },
  {
    id: 'it-dimas',
    name: 'Dimas Pratama',
    targetJob: 'IT00001 - Backend Engineer',
    fileName: 'cv_it00001_dimas_pratama_high_match.pdf',
    path: '/example-cvs/cv_it00001_dimas_pratama_high_match.pdf',
  },
];

export function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [processingFiles, setProcessingFiles] = useState<Map<string, ProcessingProgress>>(new Map());
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [loadingExampleId, setLoadingExampleId] = useState<string | null>(null);
  const { addCandidate, candidates, removeCandidate, updateCandidate } = useAppStore();

  // Only allow 1 CV at a time
  const existingCandidate = candidates[0] ?? null;

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const processSingleFile = async (file: File, displayName?: string) => {
    // Clear any existing candidate first
    if (existingCandidate) {
      removeCandidate(existingCandidate.id);
    }

    const id = generateUUID();
    const candidate: Candidate = {
      id,
      name: displayName ?? file.name.replace(/\.[^/.]+$/, ''),
      fileName: file.name,
      extractedText: '',
      status: 'processing',
      createdAt: new Date(),
    };

    addCandidate(candidate);

    try {
      const result = await processFile(file, (progress) => {
        setProcessingFiles((prev) => new Map(prev).set(id, progress));
      });

      updateCandidate(id, {
        extractedText: result.text,
        status: 'completed',
      });
    } catch (error) {
      updateCandidate(id, {
        status: 'error',
        errorMessage: error instanceof Error ? error.message : 'Processing failed',
      });
    } finally {
      setProcessingFiles((prev) => {
        const next = new Map(prev);
        next.delete(id);
        return next;
      });
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const pdfFile = Array.from(e.dataTransfer.files).find(
      (file) => file.type === 'application/pdf'
    );

    if (pdfFile) {
      processSingleFile(pdfFile);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const pdfFile = Array.from(e.target.files || []).find(
      (file) => file.type === 'application/pdf'
    );

    if (pdfFile) {
      processSingleFile(pdfFile);
    }
    e.target.value = '';
  };

  const handleExampleSelect = async (example: typeof EXAMPLE_CVS[number]) => {
    try {
      setLoadingExampleId(example.id);
      const response = await fetch(example.path);

      if (!response.ok) {
        throw new Error(`Failed to load ${example.fileName}`);
      }

      const blob = await response.blob();
      const file = new File([blob], example.fileName, { type: 'application/pdf' });
      await processSingleFile(file, example.name);
    } catch (error) {
      const id = generateUUID();
      addCandidate({
        id,
        name: example.name,
        fileName: example.fileName,
        extractedText: '',
        status: 'error',
        errorMessage: error instanceof Error ? error.message : 'Failed to load example CV',
        createdAt: new Date(),
      });
    } finally {
      setLoadingExampleId(null);
    }
  };

  const handleRemove = (id: string) => {
    removeCandidate(id);
  };

  const handleViewExtractedText = (candidate: Candidate) => {
    if (candidate.status === 'completed' && candidate.extractedText) {
      setSelectedCandidate(candidate);
      setDialogOpen(true);
    }
  };

  const getStatusColor = (status: Candidate['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${isDragging ? 'border-primary bg-primary/5' : 'border-muted-foreground/25'}
        `}
      >
        <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
        <p className="text-lg font-medium mb-2">
          Drag and drop your CV here
        </p>
        <p className="text-sm text-muted-foreground mb-4">
          Only PDF files are accepted
        </p>
        <input
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
        />
        <Button asChild variant="outline">
          <label htmlFor="file-upload" className="cursor-pointer">
            Browse PDF
          </label>
        </Button>
      </div>

      <div className="space-y-2">
        <h3 className="text-sm font-medium text-muted-foreground">Example CVs</h3>
        <div className="grid grid-cols-1 gap-2">
          {EXAMPLE_CVS.map((example) => {
            const isLoading = loadingExampleId === example.id;

            return (
              <Button
                key={example.id}
                type="button"
                variant="outline"
                className="h-auto justify-start px-3 py-3 text-left"
                onClick={() => handleExampleSelect(example)}
                disabled={loadingExampleId !== null}
              >
                <div className="flex w-full items-start gap-3">
                  {isLoading ? (
                    <Loader2 className="mt-0.5 h-4 w-4 flex-shrink-0 animate-spin text-primary" />
                  ) : (
                    <FileText className="mt-0.5 h-4 w-4 flex-shrink-0 text-muted-foreground" />
                  )}
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium">{example.name}</p>
                    <p className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Briefcase className="h-3 w-3 flex-shrink-0" />
                      <span className="truncate">{example.targetJob}</span>
                    </p>
                  </div>
                </div>
              </Button>
            );
          })}
        </div>
      </div>

      {existingCandidate && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-muted-foreground">Uploaded CV</h3>
          <Card
            className={`p-3 ${existingCandidate.status === 'completed' && existingCandidate.extractedText ? 'cursor-pointer hover:bg-accent/50 transition-colors' : ''}`}
            onClick={() => handleViewExtractedText(existingCandidate)}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 flex-1 min-w-0">
                <FileText className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium truncate">
                    {existingCandidate.name}
                  </p>
                  {existingCandidate.status === 'completed' && (
                    <p className="text-xs text-muted-foreground flex items-center gap-1">
                      <span className="text-primary flex items-center gap-0.5">
                        <Eye className="h-3 w-3" />
                        Click to view text
                      </span>
                    </p>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2 ml-2">
                <Badge
                  variant="secondary"
                  className={getStatusColor(existingCandidate.status)}
                >
                  {existingCandidate.status === 'processing' && processingFiles.get(existingCandidate.id) && (
                    <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                  )}
                  {existingCandidate.status}
                </Badge>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleRemove(existingCandidate.id);
                  }}
                  disabled={existingCandidate.status === 'processing'}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
            {processingFiles.get(existingCandidate.id) && existingCandidate.status === 'processing' && (
              <div className="mt-2 space-y-1">
                <Progress value={processingFiles.get(existingCandidate.id)!.progress} className="h-2" />
                <p className="text-xs text-muted-foreground">
                  {processingFiles.get(existingCandidate.id)!.message}
                </p>
              </div>
            )}
            {existingCandidate.status === 'error' && existingCandidate.errorMessage && (
              <p className="text-xs text-red-500 mt-2">
                {existingCandidate.errorMessage}
              </p>
            )}
          </Card>
        </div>
      )}

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[80vh] flex flex-col">
          <DialogHeader>
            <DialogTitle>Extracted Text - {selectedCandidate?.name}</DialogTitle>
            <DialogDescription>
              PDF text extraction completed successfully
            </DialogDescription>
          </DialogHeader>
          <ScrollArea className="flex-1 mt-4 rounded-md border p-4">
            <pre className="text-sm whitespace-pre-wrap font-mono">
              {selectedCandidate?.extractedText || 'No text extracted'}
            </pre>
          </ScrollArea>
        </DialogContent>
      </Dialog>
    </div>
  );
}
