import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import {
  Upload,
  ChevronLeft,
  ChevronRight,
  ZoomIn,
  ZoomOut,
  Loader2,
} from "lucide-react";

// Standard CSS imports for react-pdf
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface PDFViewerProps {
  onTextSelect: (text: string) => void;
}

const PDFViewer = ({ onTextSelect }: PDFViewerProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [scale, setScale] = useState<number>(1);

  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPageNumber(1);
    }
  };

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  // Auto capture selected text
  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim().length > 3) {
      onTextSelect(selection.toString().trim());
    }
  };

  return (
    <div className="flex h-full flex-col rounded-xl border border-gray-200 bg-gray-50/50 dark:border-gray-800 dark:bg-gray-900/20">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-950">
        <h2 className="font-semibold text-gray-900 dark:text-gray-100">PDF Viewer</h2>

        <label className="cursor-pointer flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-700 transition-colors">
          <Upload size={14} />
          Upload PDF
          <input
            type="file"
            accept="application/pdf"
            onChange={onFileChange}
            className="hidden"
          />
        </label>
      </div>

      {/* PDF Display Area */}
      <div
        className="flex-1 overflow-auto p-4 flex justify-center bg-gray-100 dark:bg-gray-900"
        onMouseUp={handleTextSelection}
      >
        {!file ? (
          <div className="flex h-full flex-col items-center justify-center">
            <Upload size={48} className="mb-4 text-gray-400" />
            <p className="text-sm text-gray-500">Upload a PDF to get started</p>
          </div>
        ) : (
          <div className="shadow-lg border border-gray-200 dark:border-gray-700 bg-white">
            <Document
              file={file}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={
                <div className="flex flex-col items-center p-20 gap-2">
                  <Loader2 className="animate-spin text-blue-500" />
                  <p className="text-sm text-gray-500">Loading PDF...</p>
                </div>
              }
              error={
                <div className="p-10 text-center text-red-500">
                  <p className="font-bold">Failed to load PDF.</p>
                  <p className="text-xs">Check console for worker errors or try a different file.</p>
                </div>
              }
            >
              <Page
                pageNumber={pageNumber}
                scale={scale}
                renderTextLayer={true}
                renderAnnotationLayer={true}
                // Important for responsiveness
                width={Math.min(window.innerWidth * 0.8, 800)}
              />
            </Document>
          </div>
        )}
      </div>

      {/* Controls Bar */}
      {file && numPages > 0 && (
        <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-800 dark:bg-gray-950">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <button
                onClick={() => setPageNumber((prev) => Math.max(1, prev - 1))}
                disabled={pageNumber <= 1}
                className="rounded p-1 hover:bg-gray-100 disabled:opacity-30 dark:hover:bg-gray-800"
              >
                <ChevronLeft size={20} />
              </button>
              <span className="text-sm font-medium min-w-[80px] text-center">
                {pageNumber} / {numPages}
              </span>
              <button
                onClick={() => setPageNumber((prev) => Math.min(numPages, prev + 1))}
                disabled={pageNumber >= numPages}
                className="rounded p-1 hover:bg-gray-100 disabled:opacity-30 dark:hover:bg-gray-800"
              >
                <ChevronRight size={20} />
              </button>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setScale((prev) => Math.max(0.5, prev - 0.1))}
              className="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-800"
              title="Zoom Out"
            >
              <ZoomOut size={18} />
            </button>
            <span className="text-sm font-mono w-12 text-center">
              {Math.round(scale * 100)}%
            </span>
            <button
              onClick={() => setScale((prev) => Math.min(2.5, prev + 0.1))}
              className="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-800"
              title="Zoom In"
            >
              <ZoomIn size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PDFViewer;

