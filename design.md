# AI-Powered Learning Workflow Platform - Design Document

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PDF Viewer   │  │ Sticky       │  │ Workflow     │      │
│  │ Component    │  │ Notepad UI   │  │ Visualizer   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│              (REST API + WebSocket for real-time)            │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ↓                       ↓
┌──────────────────────────┐  ┌──────────────────────────┐
│   AI Processing Service   │  │   Content Service        │
│  ┌────────────────────┐  │  │  ┌────────────────────┐ │
│  │ Concept Extractor  │  │  │  │ Text Capture       │ │
│  │ Workflow Generator │  │  │  │ Storage Manager    │ │
│  │ Summary Generator  │  │  │  │ Export Handler     │ │
│  └────────────────────┘  │  │  └────────────────────┘ │
└──────────────────────────┘  └──────────────────────────┘
                │                       │
                └───────────┬───────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PostgreSQL   │  │ Redis Cache  │  │ S3 Storage   │      │
│  │ (Metadata)   │  │ (Sessions)   │  │ (PDFs/Notes) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design

### 1. Frontend Components

#### 1.1 PDF Viewer Component
**Technology**: PDF.js or React-PDF

**Responsibilities**:
- Render PDF documents in browser
- Handle text selection events
- Maintain page context and position
- Support zoom and navigation

**Key Methods**:
```typescript
interface PDFViewerComponent {
  loadPDF(url: string): Promise<void>
  onTextSelect(callback: (text: string, context: SelectionContext) => void): void
  highlightText(pageNum: number, coordinates: TextCoordinates): void
  getCurrentPage(): number
}
```

#### 1.2 Sticky Notepad Component
**Technology**: React with local state management

**Responsibilities**:
- Display captured text segments
- Show AI processing status
- Render workflow visualization
- Handle user interactions

**State Structure**:
```typescript
interface NotepadState {
  capturedTexts: CapturedText[]
  currentWorkflow: Workflow | null
  isProcessing: boolean
  autoSaveStatus: 'saved' | 'saving' | 'error'
}
```

#### 1.3 Workflow Visualizer
**Technology**: React Flow or D3.js

**Responsibilities**:
- Display learning steps as nodes
- Show dependencies and sequence
- Enable step reordering
- Visualize progress

---

### 2. Backend Services

#### 2.1 AI Processing Service

**Technology Stack**:
- Python FastAPI
- LangChain for LLM orchestration
- OpenAI GPT-4 or Google Gemini API
- Sentence Transformers for embeddings

**Core Modules**:

##### Concept Extractor
```python
class ConceptExtractor:
    def extract_concepts(self, text: str) -> List[Concept]:
        """
        Extract key concepts from captured text using NLP
        Returns list of concepts with importance scores
        """
        
    def identify_relationships(self, concepts: List[Concept]) -> ConceptGraph:
        """
        Build dependency graph between concepts
        """
```

##### Workflow Generator
```python
class WorkflowGenerator:
    def generate_workflow(self, concepts: List[Concept], 
                         graph: ConceptGraph) -> Workflow:
        """
        Create optimal learning sequence using topological sort
        and educational best practices
        """
        
    def optimize_sequence(self, workflow: Workflow) -> Workflow:
        """
        Apply learning science principles to optimize order
        """
```

##### Summary Generator
```python
class SummaryGenerator:
    def generate_summary(self, step: WorkflowStep, 
                        context: LearningContext) -> Summary:
        """
        Generate contextual summary for a learning step
        Uses LLM with educational prompting
        """
        
    def adapt_language(self, summary: Summary, 
                      language: str) -> Summary:
        """
        Translate and adapt summary to target language
        """
```

**AI Prompting Strategy**:

For Workflow Generation:
```
You are an expert educational AI. Analyze the following concepts extracted 
from a student's study material:

{concepts}

Create a structured learning workflow that:
1. Orders concepts from foundational to advanced
2. Groups related concepts together
3. Identifies prerequisite relationships
4. Suggests optimal learning sequence

Output format: JSON with steps, dependencies, and rationale
```

For Summary Generation:
```
You are a patient tutor explaining concepts to a student. 

Context: This is step {step_number} of {total_steps} in learning about {topic}
Previous concepts covered: {previous_concepts}

Generate a clear, concise summary (150-200 words) that:
1. Explains the core concept simply
2. Connects to previously learned material
3. Provides a practical example
4. Highlights key takeaways

Content to summarize:
{step_content}
```

#### 2.2 Content Service

**Technology Stack**:
- Node.js with Express or Python FastAPI
- PostgreSQL for metadata
- Redis for caching
- AWS S3 or MinIO for file storage

**Core Modules**:

##### Text Capture Handler
```typescript
class TextCaptureHandler {
  async captureText(
    userId: string,
    pdfId: string,
    text: string,
    context: SelectionContext
  ): Promise<CapturedText>
  
  async getCapturedTexts(
    userId: string,
    pdfId: string
  ): Promise<CapturedText[]>
}
```

##### Storage Manager
```typescript
class StorageManager {
  async saveWorkflow(workflow: Workflow): Promise<string>
  async getWorkflow(workflowId: string): Promise<Workflow>
  async saveStudyNotes(notes: StudyNotes): Promise<string>
  async autoSave(sessionId: string, data: any): Promise<void>
}
```

##### Export Handler
```typescript
class ExportHandler {
  async exportToPDF(workflowId: string): Promise<Buffer>
  async exportToMarkdown(workflowId: string): Promise<string>
  async generateDownloadLink(fileId: string): Promise<string>
}
```

---

## Data Models

### Core Entities

```typescript
interface CapturedText {
  id: string
  userId: string
  pdfId: string
  text: string
  pageNumber: number
  coordinates: TextCoordinates
  timestamp: Date
  context: string // surrounding text for context
}

interface Concept {
  id: string
  name: string
  description: string
  importance: number // 0-1 score
  keywords: string[]
  sourceTextIds: string[] // references to CapturedText
}

interface ConceptGraph {
  concepts: Concept[]
  edges: ConceptEdge[]
}

interface ConceptEdge {
  from: string // concept id
  to: string // concept id
  relationship: 'prerequisite' | 'related' | 'builds-on'
  strength: number // 0-1
}

interface Workflow {
  id: string
  userId: string
  pdfId: string
  title: string
  steps: WorkflowStep[]
  createdAt: Date
  updatedAt: Date
  status: 'draft' | 'in-progress' | 'completed'
}

interface WorkflowStep {
  id: string
  order: number
  title: string
  conceptIds: string[]
  summary: Summary | null
  estimatedTime: number // minutes
  completed: boolean
  dependencies: string[] // step ids that must be completed first
}

interface Summary {
  id: string
  stepId: string
  content: string
  language: string
  keyPoints: string[]
  examples: string[]
  generatedAt: Date
}

interface StudyNotes {
  id: string
  workflowId: string
  userId: string
  title: string
  content: string // formatted markdown
  exportFormat: 'pdf' | 'markdown' | 'html'
  createdAt: Date
}
```

### Database Schema

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- PDFs table
CREATE TABLE pdfs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  filename VARCHAR(255),
  storage_url TEXT,
  uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Captured texts table
CREATE TABLE captured_texts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  pdf_id UUID REFERENCES pdfs(id),
  text TEXT NOT NULL,
  page_number INTEGER,
  coordinates JSONB,
  context TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Workflows table
CREATE TABLE workflows (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  pdf_id UUID REFERENCES pdfs(id),
  title VARCHAR(255),
  steps JSONB NOT NULL,
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Summaries table
CREATE TABLE summaries (
  id UUID PRIMARY KEY,
  workflow_id UUID REFERENCES workflows(id),
  step_id VARCHAR(255),
  content TEXT NOT NULL,
  language VARCHAR(10),
  key_points JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Study notes table
CREATE TABLE study_notes (
  id UUID PRIMARY KEY,
  workflow_id UUID REFERENCES workflows(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(255),
  content TEXT,
  export_format VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_captured_texts_user_pdf ON captured_texts(user_id, pdf_id);
CREATE INDEX idx_workflows_user ON workflows(user_id);
CREATE INDEX idx_workflows_status ON workflows(status);
```

---

## API Design

### REST Endpoints

#### Text Capture
```
POST /api/v1/capture
Body: {
  pdfId: string,
  text: string,
  pageNumber: number,
  coordinates: object,
  context: string
}
Response: { capturedTextId: string }
```

#### Generate Workflow
```
POST /api/v1/workflows/generate
Body: {
  pdfId: string,
  capturedTextIds: string[]
}
Response: {
  workflowId: string,
  workflow: Workflow
}
```

#### Generate Summary
```
POST /api/v1/summaries/generate
Body: {
  workflowId: string,
  stepId: string,
  language?: string
}
Response: {
  summary: Summary
}
```

#### Export Study Notes
```
POST /api/v1/export
Body: {
  workflowId: string,
  format: 'pdf' | 'markdown'
}
Response: {
  downloadUrl: string,
  expiresAt: Date
}
```

#### Get User Workflows
```
GET /api/v1/workflows?userId={userId}&status={status}
Response: {
  workflows: Workflow[]
}
```

### WebSocket Events

```typescript
// Client -> Server
{
  type: 'TEXT_CAPTURED',
  payload: CapturedText
}

// Server -> Client
{
  type: 'WORKFLOW_GENERATION_STARTED',
  payload: { workflowId: string }
}

{
  type: 'WORKFLOW_GENERATION_PROGRESS',
  payload: { progress: number, currentStep: string }
}

{
  type: 'WORKFLOW_GENERATION_COMPLETE',
  payload: { workflow: Workflow }
}

{
  type: 'AUTO_SAVE_COMPLETE',
  payload: { timestamp: Date }
}
```

---

## AI Model Selection

### Primary LLM Options

**Option 1: OpenAI GPT-4 Turbo**
- Pros: Excellent reasoning, multilingual support, reliable
- Cons: Cost per token, API dependency
- Use case: Production deployment

**Option 2: Google Gemini Pro**
- Pros: Cost-effective, good performance, free tier
- Cons: Rate limits on free tier
- Use case: Hackathon demo, MVP

**Option 3: Open-source (Llama 3 or Mistral)**
- Pros: No API costs, full control, privacy
- Cons: Requires GPU infrastructure, more setup
- Use case: Future self-hosted option


## User Experience Flow

### Primary User Journey

1. **PDF Loading**
   - User uploads or opens PDF in platform
   - PDF renders in viewer with sticky notepad overlay
   - System creates session and initializes auto-save

2. **Text Capture**
   - User selects text in PDF
   - Text instantly appears in sticky notepad
   - Visual confirmation (highlight + animation)
   - Auto-save triggers

3. **Workflow Generation Trigger**
   - After 2+ text captures, AI button appears
   - User clicks "Generate Learning Workflow"
   - Loading state with progress indicator
   - AI analyzes content (5-10 seconds)

4. **Workflow Review**
   - AI presents structured learning path
   - Steps shown as visual flowchart
   - User can reorder or modify steps
   - "Generate Summaries" button enabled

5. **Summary Generation**
   - AI generates summary for each step
   - Summaries appear progressively
   - User can regenerate any summary
   - Language selection available

6. **Save and Export**
   - Auto-save runs continuously
   - User clicks "Export as PDF"
   - Download link generated
   - Success confirmation

7. **Revisit**
   - User accesses "My Study Notes"
   - Browse saved workflows
   - Search and filter options
   - One-click to resume or export

---

## Performance Optimization

### Frontend Optimization
- Lazy load PDF pages
- Virtual scrolling for long documents
- Debounce text selection events
- Cache rendered workflow visualizations
- Service worker for offline support

### Backend Optimization
- Redis caching for frequently accessed workflows
- Batch AI requests when possible
- Async processing for non-critical operations
- CDN for static assets and exported PDFs
- Database query optimization with proper indexes

### AI Optimization
- Prompt caching for repeated patterns
- Streaming responses for summaries
- Parallel processing for independent steps
- Token usage optimization
- Fallback to smaller models for simple tasks

---


## Technology Stack Summary

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- PDF.js for PDF rendering
- React Flow for workflow visualization
- Zustand for state management
- Socket.io-client for real-time updates

### Backend
- Python FastAPI (AI service)
- Node.js Express (Content service)
- PostgreSQL (primary database)
- Redis (caching and sessions)
- S3-compatible storage (files)

### AI/ML
- LangChain for LLM orchestration
- Google Gemini Pro API
- Sentence Transformers for embeddings
- NetworkX for graph algorithms

### DevOps
- Docker for containerization
- GitHub Actions for CI/CD
- Vercel for frontend deployment
- Railway for backend deployment

---
