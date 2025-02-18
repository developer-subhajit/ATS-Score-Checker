"""
File upload and management endpoints.
"""

import logging
import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ...preprocessing import DataManager
from ..models.requests import FileMetadata
from ..models.responses import FileListResponse, FileResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize data manager
data_manager = DataManager()


@router.post("/resume", response_model=FileResponse)
async def upload_resume(file: UploadFile = File(...), metadata: Optional[FileMetadata] = None) -> FileResponse:
    """
    Upload a resume file (PDF, DOCX, or TXT).
    """
    try:
        # Validate file type
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ]:
            raise HTTPException(
                status_code=400, detail="Invalid file type. Only PDF, DOCX, and TXT files are supported."
            )

        # Check file size (10MB limit)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        file_size = 0
        content = []

        # Read file in chunks
        chunk_size = 1024 * 1024  # 1MB chunks
        while chunk := await file.read(chunk_size):
            content.append(chunk)
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400, detail=f"File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB"
                )

        # Generate unique ID
        file_id = str(uuid.uuid4())

        # Save file temporarily
        temp_path = f"data/raw/{file_id}_{file.filename}"
        with open(temp_path, "wb") as f:
            for chunk in content:
                f.write(chunk)

        # Process resume
        try:
            result = data_manager.save_resume(temp_path)
        except Exception as e:
            # Clean up temp file if processing fails
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(status_code=400, detail=str(e))

        return FileResponse(
            file_id=file_id,
            file_name=file.filename,
            file_type=result["file_type"],
            file_size=result["file_size"],
            uploaded_at=datetime.now(),
            metadata=metadata.dict() if metadata else None,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing resume")


@router.post("/job", response_model=FileResponse)
async def upload_job_description(file: UploadFile = File(...), metadata: Optional[FileMetadata] = None) -> FileResponse:
    """
    Upload a job description file (PDF, DOCX, or TXT).
    """
    try:
        # Validate file type
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Generate unique ID
        file_id = str(uuid.uuid4())

        # Save file temporarily
        temp_path = f"data/raw/{file_id}_{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Process job description
        result = data_manager.save_job_description(
            temp_path,
            job_title=metadata.title if metadata else file.filename,
            company=metadata.company if metadata else None,
        )

        return FileResponse(
            file_id=file_id,
            file_name=file.filename,
            file_type=result["file_type"],
            file_size=result["file_size"],
            uploaded_at=datetime.now(),
            metadata=metadata.dict() if metadata else None,
        )

    except Exception as e:
        logger.error(f"Error uploading job description: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing job description")


@router.post("/job/text", response_model=FileResponse)
async def upload_job_description_text(
    text: str = Form(...), title: Optional[str] = Form(None), company: Optional[str] = Form(None)
) -> FileResponse:
    """
    Upload job description as text.
    """
    try:
        # Validate text content
        if not text.strip():
            raise HTTPException(status_code=400, detail="Job description text cannot be empty")

        if len(text) > 50000:  # Limit text to 50KB
            raise HTTPException(status_code=400, detail="Text content too large. Maximum size is 50KB")

        # Generate unique ID
        file_id = str(uuid.uuid4())

        # Save text to temporary file
        temp_path = f"data/raw/{file_id}_job.txt"
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Process job description
        try:
            result = data_manager.save_job_description(temp_path, job_title=title or "Untitled Job", company=company)
        except Exception as e:
            # Clean up temp file if processing fails
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(status_code=400, detail=str(e))

        return FileResponse(
            file_id=file_id,
            file_name="job.txt",
            file_type="txt",
            file_size=len(text.encode("utf-8")),
            uploaded_at=datetime.now(),
            metadata={"title": title, "company": company} if title or company else None,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing job description text: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing job description")


@router.get("/resumes", response_model=FileListResponse)
async def list_resumes() -> FileListResponse:
    """
    List all uploaded resumes.
    """
    try:
        resumes = data_manager.get_processed_resumes()
        return FileListResponse(
            files=[
                FileResponse(
                    file_id=str(uuid.uuid4()),  # In production, store and retrieve actual IDs
                    file_name=resume["original_file"],
                    file_type=resume["file_type"],
                    file_size=resume["file_size"],
                    uploaded_at=datetime.fromisoformat(resume["processed_at"]),
                    metadata=None,
                )
                for resume in resumes
            ],
            total=len(resumes),
        )
    except Exception as e:
        logger.error(f"Error listing resumes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving resumes")


@router.get("/jobs", response_model=FileListResponse)
async def list_jobs() -> FileListResponse:
    """
    List all uploaded job descriptions.
    """
    try:
        jobs = data_manager.get_job_descriptions()
        return FileListResponse(
            files=[
                FileResponse(
                    file_id=str(uuid.uuid4()),  # In production, store and retrieve actual IDs
                    file_name=job["original_file"],
                    file_type=job["file_type"],
                    file_size=job["file_size"],
                    uploaded_at=datetime.fromisoformat(job["processed_at"]),
                    metadata={"title": job.get("job_title"), "company": job.get("company")},
                )
                for job in jobs
            ],
            total=len(jobs),
        )
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving jobs")


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """
    Delete a file by ID.
    """
    try:
        # In production, implement actual file deletion
        return {"message": f"File {file_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting file")
