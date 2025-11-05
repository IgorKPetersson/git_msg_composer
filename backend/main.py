"""
Main FastAPI application for Git Commit Message Composer
WHY FastAPI? It's modern, fast, and has automatic API documentation
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# WHY? So we can access GEMINI_API_KEY and other config
load_dotenv()

from git_analyzer import GitAnalyzer
from gemini_service import GeminiService
from database import Database

app = FastAPI(
    title="Git Commit Message Composer",
    description="AI-powered commit message generator using Google Gemini",
    version="1.0.0"
)

# CORS middleware - allows frontend to communicate with backend
# WHY? Frontend (React) runs on different port than backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
git_analyzer = GitAnalyzer()
gemini_service = GeminiService()
db = Database()

# Request/Response models - defines data structure
class AnalyzeRequest(BaseModel):
    repo_path: Optional[str] = None  # If None, uses current directory

class CommitMessageResponse(BaseModel):
    message: str
    type: str  # feat, fix, docs, etc.
    files_changed: list[str]
    insertions: int
    deletions: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Git Commit Message Composer API"}

@app.post("/analyze", response_model=CommitMessageResponse)
async def analyze_changes(request: AnalyzeRequest):
    """
    Analyze git changes and generate commit message

    WHY this endpoint? It's the main feature - analyzing code and creating messages
    """
    try:
        # Step 1: Get git diff (what changed in the code)
        repo_path = request.repo_path or os.getcwd()
        diff_data = git_analyzer.get_staged_changes(repo_path)

        if not diff_data["has_changes"]:
            raise HTTPException(status_code=400, detail="No staged changes found")

        # Step 2: Send to Gemini AI for analysis
        commit_message = await gemini_service.generate_commit_message(
            diff=diff_data["diff"],
            files=diff_data["files"]
        )

        # Step 3: Save to database for history
        db.save_commit(
            message=commit_message["message"],
            commit_type=commit_message["type"],
            files=diff_data["files"]
        )

        # Step 4: Return the result
        return CommitMessageResponse(
            message=commit_message["message"],
            type=commit_message["type"],
            files_changed=diff_data["files"],
            insertions=diff_data["insertions"],
            deletions=diff_data["deletions"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(limit: int = 10):
    """Get recent commit message history"""
    try:
        history = db.get_recent_commits(limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regenerate")
async def regenerate_message(request: AnalyzeRequest):
    """Regenerate commit message with different style"""
    # Same as analyze but can add variations
    return await analyze_changes(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
