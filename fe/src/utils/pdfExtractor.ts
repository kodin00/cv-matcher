import * as pdfjsLib from 'pdfjs-dist';
import pdfWorker from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import type { ProcessingProgress } from '@/types';

// PDF.js worker setup - use local bundled worker instead of CDN
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

export async function processFile(
  file: File,
  onProgress?: (progress: ProcessingProgress) => void
): Promise<{ text: string }> {
  try {
    onProgress?.({
      status: 'loading',
      progress: 10,
      message: 'Loading file...',
    });

    if (file.type !== 'application/pdf') {
      throw new Error('Only PDF files are supported.');
    }

    return await processPDF(file, onProgress);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    onProgress?.({
      status: 'error',
      progress: 0,
      message: errorMessage,
    });
    throw error;
  }
}

async function processPDF(
  file: File,
  onProgress?: (progress: ProcessingProgress) => void
): Promise<{ text: string }> {
  const arrayBuffer = await file.arrayBuffer();

  onProgress?.({
    status: 'processing',
    progress: 20,
    message: 'Reading PDF...',
  });

  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  const numPages = pdf.numPages;

  let fullText = '';

  // Process first 5 pages only (CVs are typically 1-3 pages)
  const pagesToProcess = Math.min(numPages, 5);

  for (let i = 1; i <= pagesToProcess; i++) {
    onProgress?.({
      status: 'processing',
      progress: 20 + (i / pagesToProcess) * 70,
      message: `Extracting text from page ${i} of ${pagesToProcess}...`,
    });

    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    const pageText = textContent.items
      .map((item) => {
        if ('str' in item) return item.str;
        return '';
      })
      .join(' ');

    fullText += pageText + '\n';

    // Cleanup
    page.cleanup();
  }

  onProgress?.({
    status: 'completed',
    progress: 100,
    message: 'Text extraction completed',
  });

  return {
    text: fullText.trim(),
  };
}
