import { useState } from 'react';
import PDFViewer from './PDFViewer';
import { ArrowLeft, Copy, Trash2 } from 'lucide-react'; // CHANGED: added ArrowLeft

interface WorkspaceProps { // NEW
  onBack?: () => void;
}

const Workspace = ({ onBack }: WorkspaceProps) => { // CHANGED: accept onBack prop
  const [notes, setNotes] = useState<string[]>([]);
  const [currentNote, setCurrentNote] = useState('');

  const handleTextCapture = (text: string) => {
    setNotes(prev => [...prev, text]);
    setCurrentNote(prev => 
      prev ? `${prev}\n\n${text}` : text
    );
  };

  return (
    <div className="fixed inset-0 bg-background pt-20">
      {/* NEW: Back button */}
      {onBack && (
        <button
          onClick={onBack}
          className="fixed left-4 top-4 z-50 flex items-center gap-1 rounded-lg border border-border bg-card px-3 py-2 text-xs font-semibold text-foreground shadow-md hover:bg-secondary"
        >
          <ArrowLeft size={14} />
          Back
        </button>
      )}

      <div className="flex h-full gap-4 p-4">
        {/* PDF Viewer - Left Side (70%) */}
        <div className="flex-[7]">
          <PDFViewer onTextSelect={handleTextCapture} />
        </div>

        {/* Notepad - Right Side (30%) */}
        <div className="flex-[3]">
          <div className="h-full rounded-xl border border-border bg-card shadow-2xl">
            <div className="flex h-full flex-col">
              <div className="border-b border-border bg-secondary/50 px-4 py-3">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>
                  <h3 className="font-semibold text-foreground">Smart Notepad</h3>
                  <span className="text-xs text-muted-foreground">
                    ({notes.length} captures)
                  </span>
                </div>
              </div>

              <div className="border-b border-border bg-primary/5 px-4 py-2">
                <p className="text-xs text-muted-foreground">
                  ✨ Select text in PDF - Auto-captured instantly!
                </p>
              </div>

              <div className="flex-1 overflow-y-auto p-4">
                {notes.length === 0 ? (
                  <div className="flex h-full items-center justify-center text-center">
                    <p className="text-sm text-muted-foreground">
                      Upload a PDF and select text to start capturing!
                    </p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {notes.map((note, index) => (
                      <div
                        key={index}
                        className="group relative rounded-lg border border-border bg-secondary/30 p-3 text-xs"
                      >
                        <button
                          onClick={() => {
                            setNotes(prev => prev.filter((_, i) => i !== index));
                            const newNotes = notes.filter((_, i) => i !== index);
                            setCurrentNote(newNotes.join('\n\n'));
                          }}
                          className="absolute right-2 top-2 hidden rounded p-1 hover:bg-destructive group-hover:block"
                        >
                          <Trash2 size={12} className="text-destructive-foreground" />
                        </button>
                        <p className="pr-6">{note}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex-1 border-t border-border p-4">
                <textarea
                  value={currentNote}
                  onChange={(e) => setCurrentNote(e.target.value)}
                  placeholder="All captured text appears here..."
                  className="h-full w-full resize-none rounded-lg border border-border bg-background p-3 text-sm focus:border-primary focus:outline-none"
                />
              </div>

              <div className="border-t border-border bg-secondary/50 px-4 py-3">
                <div className="flex justify-between">
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(currentNote);
                      alert('All notes copied to clipboard!');
                    }}
                    disabled={!currentNote}
                    className="flex items-center gap-1 rounded-lg bg-primary px-4 py-2 text-xs font-semibold text-white hover:bg-primary/90 disabled:opacity-50"
                  >
                    <Copy size={14} />
                    Copy All
                  </button>
                  <button
                    onClick={() => {
                      if (confirm('Clear all notes?')) {
                        setNotes([]);
                        setCurrentNote('');
                      }
                    }}
                    disabled={notes.length === 0}
                    className="flex items-center gap-1 rounded-lg border border-border px-4 py-2 text-xs font-semibold hover:bg-secondary disabled:opacity-50"
                  >
                    <Trash2 size={14} />
                    Clear
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Workspace;
