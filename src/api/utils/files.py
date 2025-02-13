"""
File handling utilities for the API.
"""

import logging
import os
import shutil
from typing import List

from fastapi import HTTPException, UploadFile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported file types
SUPPORTED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt",
}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """
    Save an uploaded file to the specified destination.

    Args:
        upload_file: FastAPI UploadFile object
        destination: Destination path

    Returns:
        Path to the saved file

    Raises:
        HTTPException: If file is invalid or save fails
    """
    try:
        # Validate file type
        if upload_file.content_type not in SUPPORTED_MIME_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {upload_file.content_type}")

        # Validate file size
        file_size = 0
        content = []

        # Read file in chunks to check size
        chunk_size = 1024 * 1024  # 1MB chunks
        async for chunk in upload_file.stream():
            content.append(chunk)
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400, detail=f"File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB"
                )

        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        # Write file
        with open(destination, "wb") as f:
            for chunk in content:
                f.write(chunk)

        return destination

    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving file")


def delete_file(file_path: str) -> bool:
    """
    Delete a file.

    Args:
        file_path: Path to the file to delete

    Returns:
        True if file was deleted, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        return False


def get_file_extension(content_type: str) -> str:
    """
    Get file extension from MIME type.

    Args:
        content_type: MIME type string

    Returns:
        File extension (with dot)

    Raises:
        ValueError: If MIME type is not supported
    """
    if content_type not in SUPPORTED_MIME_TYPES:
        raise ValueError(f"Unsupported MIME type: {content_type}")
    return SUPPORTED_MIME_TYPES[content_type]
