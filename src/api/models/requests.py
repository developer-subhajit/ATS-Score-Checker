"""
Request models for API endpoints.
"""

from typing import Optional

from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    """Request model for score calculation."""

    resume_id: str = Field(..., description="ID of the uploaded resume")
    job_id: str = Field(..., description="ID of the uploaded job description")


class FileMetadata(BaseModel):
    """Optional metadata for file uploads."""

    title: Optional[str] = Field(None, description="Title or name of the document")
    company: Optional[str] = Field(None, description="Company name for job descriptions")
    description: Optional[str] = Field(None, description="Additional description")
