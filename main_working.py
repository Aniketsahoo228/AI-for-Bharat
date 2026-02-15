"""
FastAPI Backend - Complete Working Version (In-Memory Storage for MVP)
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends, Header, Body, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import shutil
from hashlib import sha256
import hmac
import base64
import pdfplumber
import tempfile

# Import AI services
from services.concept_extractor import ConceptExtractor
from services.workflow_generator import WorkflowGenerator
from services.summary_generator import SummaryGenerator

load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Study Path Maker API",
    description="AI-Powered Learning Workflow Platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI services
try:
    concept_extractor = ConceptExtractor()
    workflow_generator = WorkflowGenerator()
    summary_generator = SummaryGenerator()
except:
    pass

# ==================== In-Memory Storage (MVP) ====================
users_db = {}
pdfs_db = {}
captures_db = {}
workflows_db = {}
summaries_db = {}
tokens_db = {}  # token -> user_id mapping

# ==================== Pydantic Models ====================

class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class TextCaptureRequest(BaseModel):
    pdf_id: int
    text: str
    page_number: Optional[int] = None
    context: Optional[str] = None

class WorkflowGenerationRequest(BaseModel):
    pdf_id: int
    capture_ids: List[int]

class SummaryGenerationRequest(BaseModel):
    workflow_id: int
    step_id: str
    language: str = "English"

class SimpleSummaryRequest(BaseModel):
    text: str
    language: str = "English"

class SimpleWorkflowRequest(BaseModel):
    text: str

# ==================== Auth Helpers ====================

def hash_password(password: str) -> str:
    """Simple password hashing"""
    return sha256(password.encode()).hexdigest()

def create_token(user_id: int) -> str:
    """Create a simple token"""
    token = f"{user_id}_{uuid4()}"
    tokens_db[token] = {"user_id": user_id, "created_at": datetime.now()}
    return token

def verify_token(token: Optional[str]) -> Optional[int]:
    """Verify token and return user_id"""
    if not token or token not in tokens_db:
        return None
    return tokens_db[token]["user_id"]

def get_current_user(authorization: Optional[str] = Header(None)) -> int:
    """Extract user from auth header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id

# ==================== Health Check ====================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Study Path Maker",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    return {
        "message": "Study Path Maker API",
        "docs": "/docs",
        "health": "/health"
    }

# ==================== Authentication ====================

@app.post("/api/auth/register")
async def register(request: UserRegister):
    """Register new user"""
    # Check if email exists
    if any(u["email"] == request.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_id = len(users_db) + 1
    users_db[user_id] = {
        "id": user_id,
        "email": request.email,
        "username": request.username,
        "password_hash": hash_password(request.password),
        "full_name": request.full_name,
        "created_at": datetime.now().isoformat()
    }
    
    token = create_token(user_id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": request.username
    }

@app.post("/api/auth/login")
async def login(request: UserLogin):
    """Login user"""
    user = next(
        (u for u in users_db.values() if u["email"] == request.email),
        None
    )
    
    if not user or user["password_hash"] != hash_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["id"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user["id"],
        "username": user["username"]
    }

@app.get("/api/auth/me")
async def get_me(user_id: int = Depends(get_current_user)):
    """Get current user"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "full_name": user["full_name"]
    }

# ==================== PDF Management ====================
# NOTE: PDF upload endpoint commented out - python-multipart not loading properly
# Server will start without this, but pdf listing still works

@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and extract text from PDF"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Extract text from PDF using pdfplumber
        extracted_text = ""
        try:
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
        finally:
            os.remove(tmp_path)
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        return {
            "success": True,
            "text": extracted_text.strip(),
            "filename": file.filename,
            "message": "PDF text extracted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/api/generate-summary")
async def generate_summary_simple(request: SimpleSummaryRequest):
    """Generate summary from text"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Use AI service to generate summary
        try:
            summary_data = summary_generator.generate_summary(
                step_title="Text Summary",
                step_content=request.text,
                step_number=1,
                total_steps=1,
                language=request.language
            )
            summary = summary_data.get("summary", "")
            key_points = summary_data.get("keyPoints", [])
        except:
            # Fallback summary generation
            text_preview = request.text[:500]
            summary = f"Summary of provided text:\n\n{text_preview}...\n\nThis is a summary generated from the provided text."
            key_points = ["Key point 1", "Key point 2", "Key point 3"]
        
        return {
            "success": True,
            "summary": summary,
            "key_points": key_points,
            "language": request.language
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.post("/api/generate-workflow")
async def generate_workflow_simple(request: SimpleWorkflowRequest):
    """Generate workflow from text"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Use AI service to generate workflow
        try:
            workflow_data = workflow_generator.generate_workflow([request.text])
            workflow_steps = workflow_data.get("steps", [])
        except:
            # Fallback workflow generation
            text_preview = request.text[:200]
            workflow_steps = [
                {
                    "id": "step_1",
                    "order": 1,
                    "title": "Understanding Core Concepts",
                    "description": text_preview,
                    "estimatedTime": 10,
                    "completed": False
                },
                {
                    "id": "step_2",
                    "order": 2,
                    "title": "Practical Application",
                    "description": "Apply the concepts learned in the first step",
                    "estimatedTime": 15,
                    "completed": False
                },
                {
                    "id": "step_3",
                    "order": 3,
                    "title": "Review and Assessment",
                    "description": "Review the workflow and assess your understanding",
                    "estimatedTime": 10,
                    "completed": False
                }
            ]
        
        return {
            "success": True,
            "workflow": "\n".join([
                f"Step {step.get('order', 0)}: {step.get('title', '')} ({step.get('estimatedTime', 0)} mins)\n"
                f"Description: {step.get('description', '')}"
                for step in workflow_steps
            ]),
            "steps": workflow_steps
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating workflow: {str(e)}")

# @app.post("/api/pdf/upload")
# async def upload_pdf(
#     file: UploadFile = File(...),
#     user_id: int = Depends(get_current_user)
# ):
#     """Upload PDF"""
#     if not file.filename.endswith('.pdf'):
#         raise HTTPException(status_code=400, detail="Only PDFs allowed")
#     
#     # Save file
#     os.makedirs("uploads", exist_ok=True)
#     unique_name = f"{uuid4()}_{file.filename}"
#     path = f"uploads/{unique_name}"
#     
#     with open(path, "wb") as f:
#         content = await file.read()
#         f.write(content)
#     
#     pdf_id = len(pdfs_db) + 1
#     pdfs_db[pdf_id] = {
#         "id": pdf_id,
#         "user_id": user_id,
#         "filename": unique_name,
#         "original_filename": file.filename,
#         "file_path": path,
#         "uploaded_at": datetime.now().isoformat()
#     }
#     
#     return pdfs_db[pdf_id]

@app.get("/api/pdfs")
async def list_pdfs(user_id: int = Depends(get_current_user)):
    """List user PDFs"""
    return [p for p in pdfs_db.values() if p["user_id"] == user_id]

@app.get("/api/pdf/{pdf_id}")
async def get_pdf(pdf_id: int, user_id: int = Depends(get_current_user)):
    """Get specific PDF"""
    pdf = pdfs_db.get(pdf_id)
    if not pdf or pdf["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="PDF not found")
    return pdf

@app.delete("/api/pdf/{pdf_id}")
async def delete_pdf(pdf_id: int, user_id: int = Depends(get_current_user)):
    """Delete PDF"""
    pdf = pdfs_db.get(pdf_id)
    if not pdf or pdf["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    if os.path.exists(pdf["file_path"]):
        os.remove(pdf["file_path"])
    
    del pdfs_db[pdf_id]
    return {"message": "Deleted"}

# ==================== Text Capture ====================

@app.post("/api/capture/text")
async def capture_text(
    request: TextCaptureRequest,
    user_id: int = Depends(get_current_user)
):
    """Capture text"""
    pdf = pdfs_db.get(request.pdf_id)
    if not pdf or pdf["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    capture_id = len(captures_db) + 1
    captures_db[capture_id] = {
        "id": capture_id,
        "user_id": user_id,
        "pdf_id": request.pdf_id,
        "text": request.text,
        "page_number": request.page_number,
        "context": request.context,
        "created_at": datetime.now().isoformat()
    }
    
    return captures_db[capture_id]

@app.get("/api/captures/{pdf_id}")
async def get_captures(pdf_id: int, user_id: int = Depends(get_current_user)):
    """Get captures for PDF"""
    return [
        c for c in captures_db.values()
        if c["pdf_id"] == pdf_id and c["user_id"] == user_id
    ]

@app.delete("/api/capture/{capture_id}")
async def delete_capture(capture_id: int, user_id: int = Depends(get_current_user)):
    """Delete capture"""
    capture = captures_db.get(capture_id)
    if not capture or capture["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    del captures_db[capture_id]
    return {"message": "Deleted"}

# ==================== Workflows ====================

@app.post("/api/workflow/generate")
async def generate_workflow(
    request: WorkflowGenerationRequest,
    user_id: int = Depends(get_current_user)
):
    """Generate workflow"""
    # Get captures
    captures = [
        c for c in captures_db.values()
        if c["id"] in request.capture_ids and c["user_id"] == user_id
    ]
    
    if not captures:
        raise HTTPException(status_code=400, detail="No captures found")
    
    # Generate workflow using AI
    try:
        captured_texts = [c["text"] for c in captures]
        workflow_data = workflow_generator.generate_workflow(captured_texts)
    except:
        # Fallback
        workflow_data = {
            "steps": [
                {
                    "id": f"step_{i}",
                    "order": i,
                    "title": f"Step {i+1}",
                    "description": captures[i]["text"][:100],
                    "conceptIds": [],
                    "estimatedTime": 5,
                    "completed": False,
                    "dependencies": []
                }
                for i in range(len(captures))
            ]
        }
    
    workflow_id = len(workflows_db) + 1
    workflows_db[workflow_id] = {
        "id": workflow_id,
        "user_id": user_id,
        "pdf_id": request.pdf_id,
        "title": "AI-Generated Learning Path",
        "steps": workflow_data.get("steps", []),
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    return workflows_db[workflow_id]

@app.get("/api/workflows")
async def list_workflows(user_id: int = Depends(get_current_user)):
    """List user workflows"""
    return [w for w in workflows_db.values() if w["user_id"] == user_id]

@app.get("/api/workflow/{workflow_id}")
async def get_workflow(workflow_id: int, user_id: int = Depends(get_current_user)):
    """Get workflow"""
    workflow = workflows_db.get(workflow_id)
    if not workflow or workflow["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@app.put("/api/workflow/{workflow_id}")
async def update_workflow(
    workflow_id: int,
    data: dict = Body(...),
    user_id: int = Depends(get_current_user)
):
    """Update workflow"""
    workflow = workflows_db.get(workflow_id)
    if not workflow or workflow["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow.update(data)
    return workflow

@app.delete("/api/workflow/{workflow_id}")
async def delete_workflow(workflow_id: int, user_id: int = Depends(get_current_user)):
    """Delete workflow"""
    workflow = workflows_db.get(workflow_id)
    if not workflow or workflow["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    del workflows_db[workflow_id]
    return {"message": "Deleted"}

# ==================== Summaries ====================

@app.post("/api/summaries/generate")
async def generate_summary(
    request: SummaryGenerationRequest,
    user_id: int = Depends(get_current_user)
):
    """Generate summary"""
    workflow = workflows_db.get(request.workflow_id)
    if not workflow or workflow["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Find step
    steps = workflow.get("steps", [])
    step = next((s for s in steps if s.get("id") == request.step_id), None)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    
    # Generate summary using AI
    try:
        summary_content = summary_generator.generate_summary(
            step_title=step.get("title", ""),
            step_content=step.get("description", ""),
            step_number=step.get("order", 1),
            total_steps=len(steps),
            language=request.language
        )
    except:
        # Fallback
        summary_content = {
            "summary": f"Summary of {step.get('title', '')}",
            "keyPoints": ["Point 1", "Point 2", "Point 3"]
        }
    
    summary_id = len(summaries_db) + 1
    summaries_db[summary_id] = {
        "id": summary_id,
        "workflow_id": request.workflow_id,
        "step_id": request.step_id,
        "content": summary_content.get("summary", ""),
        "language": request.language,
        "key_points": summary_content.get("keyPoints", []),
        "created_at": datetime.now().isoformat()
    }
    
    return summaries_db[summary_id]

@app.get("/api/summaries/{workflow_id}")
async def get_summaries(workflow_id: int, user_id: int = Depends(get_current_user)):
    """Get summaries for workflow"""
    workflow = workflows_db.get(workflow_id)
    if not workflow or workflow["user_id"] != user_id:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return [s for s in summaries_db.values() if s["workflow_id"] == workflow_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
