import { useState, useEffect, useRef } from "react";
import { X, Minus, Maximize2, Copy, Trash2 } from "lucide-react";
import { motion } from "framer-motion";

interface FloatingNotepadProps {
  onClose: () => void;
}

const FloatingNotepad = ({ onClose }: FloatingNotepadProps) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [notes, setNotes] = useState<string[]>([]);
  const [currentNote, setCurrentNote] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const handleCopy = async (e: ClipboardEvent) => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim()) {
        const copiedText = selection.toString();
        
        setNotes(prev => [...prev, copiedText]);
        setCurrentNote(prev => 
          prev ? `${prev}\n\n${copiedText}` : copiedText
        );
      }
    };

    document.addEventListener('copy', handleCopy);
    return () => {
      document.removeEventListener('copy', handleCopy);
    };
  }, []);

  const handleClearAll = () => {
    if (confirm('Clear all notes?')) {
      setNotes([]);
      setCurrentNote("");
    }
  };

  const handleCopyAll = async () => {
    if (currentNote) {
      await navigator.clipboard.writeText(currentNote);
      alert('All notes copied to clipboard!');
    }
  };

  const handleDeleteNote = (index: number) => {
    setNotes(prev => prev.filter((_, i) => i !== index));
  };

  if (isMinimized) {
    return (
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="fixed bottom-4 right-4 z-50"
      >
        <button
          onClick={() => setIsMinimized(false)}
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-primary/90"
        >
          <Maximize2 size={16} />
          Smart Notepad ({notes.length})
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0, y: 20 }}
      animate={{ scale: 1, opacity: 1, y: 0 }}
      className="fixed bottom-4 right-4 z-50 flex w-96 flex-col rounded-xl border border-border bg-card shadow-2xl"
      style={{ maxHeight: '600px' }}
    >
      <div className="flex items-center justify-between border-b border-border bg-secondary/50 px-4 py-3 rounded-t-xl">
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded-full bg-primary"></div>
          <h3 className="font-semibold text-foreground">Smart Notepad</h3>
          <span className="text-xs text-muted-foreground">
            ({notes.length} captures)
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsMinimized(true)}
            className="rounded p-1 hover:bg-secondary"
          >
            <Minus size={16} className="text-muted-foreground" />
          </button>
          <button
            onClick={onClose}
            className="rounded p-1 hover:bg-secondary"
          >
            <X size={16} className="text-muted-foreground" />
          </button>
        </div>
      </div>

      <div className="border-b border-border bg-primary/5 px-4 py-2">
        <p className="text-xs text-muted-foreground">
          📋 Select text anywhere and press{" "}
          <kbd className="rounded bg-secondary px-1 py-0.5 text-xs">Ctrl+C</kbd>
          {" "}to auto-capture here!
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4" style={{ maxHeight: '200px' }}>
        {notes.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Copy size={32} className="mb-2 text-muted-foreground/50" />
            <p className="text-sm text-muted-foreground">
              No captures yet. Copy text to get started!
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {notes.map((note, index) => (
              <div
                key={index}
                className="group relative rounded-lg border border-border bg-secondary/30 p-3 text-sm hover:border-primary/30"
              >
                <button
                  onClick={() => handleDeleteNote(index)}
                  className="absolute right-2 top-2 hidden rounded p-1 hover:bg-destructive group-hover:block"
                >
                  <Trash2 size={12} className="text-destructive-foreground" />
                </button>
                <p className="pr-6 text-xs text-foreground">{note}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex-1 p-4">
        <textarea
          ref={textareaRef}
          value={currentNote}
          onChange={(e) => setCurrentNote(e.target.value)}
          placeholder="All captured text will appear here... You can also type your own notes."
          className="h-full w-full resize-none rounded-lg border border-border bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none"
          style={{ minHeight: '150px' }}
        />
      </div>

      <div className="flex items-center justify-between border-t border-border bg-secondary/50 px-4 py-3 rounded-b-xl">
        <div className="flex gap-2">
          <button
            onClick={handleCopyAll}
            disabled={!currentNote}
            className="flex items-center gap-1 rounded-lg bg-primary px-3 py-1.5 text-xs font-semibold text-white hover:bg-primary/90 disabled:opacity-50"
          >
            <Copy size={14} />
            Copy All
          </button>
          <button
            onClick={handleClearAll}
            disabled={notes.length === 0}
            className="flex items-center gap-1 rounded-lg border border-border px-3 py-1.5 text-xs font-semibold hover:bg-secondary disabled:opacity-50"
          >
            <Trash2 size={14} />
            Clear
          </button>
        </div>
        <p className="text-xs text-muted-foreground">
          {currentNote.length} chars
        </p>
      </div>
    </motion.div>
  );
};

export default FloatingNotepad;
