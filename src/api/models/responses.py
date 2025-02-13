"""
Response models for API endpoints.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class FileResponse(BaseModel):
    """Response model for file uploads."""

    file_id: str = Field(..., description="Unique identifier for the file")
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File type (pdf, docx, txt)")
    file_size: int = Field(..., description="File size in bytes")
    uploaded_at: datetime = Field(..., description="Upload timestamp")
    metadata: Optional[Dict] = Field(None, description="Additional metadata")


class ScoreResponse(BaseModel):
    """Response model for score calculation."""

    resume_id: str = Field(..., description="ID of the resume")
    job_id: str = Field(..., description="ID of the job description")
    tfidf_score: float = Field(..., description="TF-IDF similarity score (0-100)")
    sbert_score: float = Field(..., description="SBERT similarity score (0-100)")
    combined_score: float = Field(..., description="Combined weighted score (0-100)")
    calculated_at: datetime = Field(..., description="Calculation timestamp")


class ErrorResponse(BaseModel):
    """Response model for errors."""

    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class FileListResponse(BaseModel):
    """Response model for file listings."""

    files: List[FileResponse] = Field(..., description="List of files")
    total: int = Field(..., description="Total number of files")


class ScoreHistoryResponse(BaseModel):
    """Response model for score history."""

    scores: List[ScoreResponse] = Field(..., description="List of scores")
    total: int = Field(..., description="Total number of scores")
