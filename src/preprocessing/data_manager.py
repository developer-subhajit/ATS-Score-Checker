"""
Data management utilities for handling resumes and job descriptions.
"""

import json
import logging
import os
import shutil
from datetime import datetime
from typing import Any, Dict, List

from .file_handlers import DocumentReader
from .text_processor import TextProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    """Manages the storage and processing of resumes and job descriptions."""

    def __init__(self, base_dir: str = "data"):
        """
        Initialize the data manager.

        Args:
            base_dir: Base directory for data storage
        """
        self.base_dir = base_dir
        self.raw_dir = os.path.join(base_dir, "raw")
        self.processed_dir = os.path.join(base_dir, "processed")
        self.jobs_dir = os.path.join(base_dir, "jobs")

        # Initialize document handlers
        self.doc_reader = DocumentReader()
        self.text_processor = TextProcessor()

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.raw_dir, self.processed_dir, self.jobs_dir]:
            os.makedirs(directory, exist_ok=True)

    def save_resume(self, file_path: str, move_file: bool = True) -> Dict[str, Any]:
        """
        Save and process a resume file.

        Args:
            file_path: Path to the resume file
            move_file: Whether to move the file to raw directory

        Returns:
            Dictionary containing processed resume data
        """
        try:
            # Read document
            doc_data = self.doc_reader.read_document(file_path)

            # Process text
            processed_text = self.text_processor.preprocess_text(doc_data["text"])

            # Generate timestamp
            timestamp = datetime.now().isoformat()

            # Create metadata
            metadata = {
                "original_file": doc_data["file_name"],
                "file_type": doc_data["file_type"],
                "file_size": doc_data["file_size"],
                "processed_at": timestamp,
                "processed_text": processed_text,
                "raw_text": doc_data["text"],
            }

            # Save processed data
            processed_file = os.path.join(self.processed_dir, f"resume_{timestamp.replace(':', '-')}.json")
            with open(processed_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            # Move original file if requested and not already in raw directory
            if move_file and not file_path.startswith(self.raw_dir):
                new_path = os.path.join(self.raw_dir, doc_data["file_name"])
                # If file already exists, add timestamp to filename
                if os.path.exists(new_path):
                    base, ext = os.path.splitext(new_path)
                    new_path = f"{base}_{timestamp.replace(':', '-')}{ext}"
                shutil.copy2(file_path, new_path)
                logger.info(f"Copied resume to {new_path}")

            logger.info(f"Successfully processed resume: {doc_data['file_name']}")
            return metadata

        except Exception as e:
            logger.error(f"Error processing resume {file_path}: {str(e)}")
            raise

    def save_job_description(self, file_path: str, job_title: str, company: str = None) -> Dict[str, Any]:
        """
        Save and process a job description.

        Args:
            file_path: Path to the job description file
            job_title: Title of the job
            company: Company name (optional)

        Returns:
            Dictionary containing processed job data
        """
        try:
            # Read document
            doc_data = self.doc_reader.read_document(file_path)

            # Process text
            processed_text = self.text_processor.preprocess_text(doc_data["text"])

            # Generate timestamp
            timestamp = datetime.now().isoformat()

            # Create metadata
            metadata = {
                "job_title": job_title,
                "company": company,
                "original_file": doc_data["file_name"],
                "file_type": doc_data["file_type"],
                "file_size": doc_data["file_size"],
                "processed_at": timestamp,
                "processed_text": processed_text,
                "raw_text": doc_data["text"],
            }

            # Save processed data
            processed_file = os.path.join(self.jobs_dir, f"job_{timestamp.replace(':', '-')}.json")
            with open(processed_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Successfully processed job description: {job_title}")
            return metadata

        except Exception as e:
            logger.error(f"Error processing job description {file_path}: {str(e)}")
            raise

    def get_processed_resumes(self) -> List[Dict[str, Any]]:
        """Get all processed resumes."""
        resumes = []
        for file in os.listdir(self.processed_dir):
            if file.startswith("resume_") and file.endswith(".json"):
                with open(os.path.join(self.processed_dir, file), "r") as f:
                    resumes.append(json.load(f))
        return resumes

    def get_job_descriptions(self) -> List[Dict[str, Any]]:
        """Get all processed job descriptions."""
        jobs = []
        for file in os.listdir(self.jobs_dir):
            if file.startswith("job_") and file.endswith(".json"):
                with open(os.path.join(self.jobs_dir, file), "r") as f:
                    jobs.append(json.load(f))
        return jobs
