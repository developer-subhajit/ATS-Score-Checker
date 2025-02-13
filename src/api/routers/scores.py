"""
Score calculation endpoints.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ...preprocessing import DataManager
from ...scoring_system import calculate_resume_match
from ..models.requests import ScoreRequest
from ..models.responses import ScoreHistoryResponse, ScoreResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize data manager
data_manager = DataManager()


@router.post("/calculate", response_model=ScoreResponse)
async def calculate_score(request: ScoreRequest) -> ScoreResponse:
    """
    Calculate similarity scores between a resume and job description.
    """
    try:
        # Get file paths from IDs
        resume_files = [f for f in os.listdir("data/raw") if f.startswith(request.resume_id)]
        job_files = [f for f in os.listdir("data/raw") if f.startswith(request.job_id)]

        if not resume_files:
            raise HTTPException(status_code=404, detail=f"Resume with ID {request.resume_id} not found")
        if not job_files:
            raise HTTPException(status_code=404, detail=f"Job description with ID {request.job_id} not found")

        resume_path = os.path.join("data/raw", resume_files[0])
        job_path = os.path.join("data/raw", job_files[0])

        # Calculate scores
        scores = calculate_resume_match(job_path, resume_path)

        return ScoreResponse(
            resume_id=request.resume_id,
            job_id=request.job_id,
            tfidf_score=scores["tfidf_score"],
            sbert_score=scores["sbert_score"],
            combined_score=scores["combined_score"],
            calculated_at=datetime.now(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating scores: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating scores")


@router.get("/history", response_model=ScoreHistoryResponse)
async def get_score_history() -> ScoreHistoryResponse:
    """
    Get history of score calculations.
    """
    try:
        # In production, implement score history storage and retrieval
        return ScoreHistoryResponse(scores=[], total=0)  # Implement actual score history
    except Exception as e:
        logger.error(f"Error retrieving score history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving score history")


@router.get("/{score_id}", response_model=ScoreResponse)
async def get_score(score_id: str) -> ScoreResponse:
    """
    Get detailed information about a specific score calculation.
    """
    try:
        # In production, implement score retrieval by ID
        raise HTTPException(status_code=404, detail="Score not found")
    except Exception as e:
        logger.error(f"Error retrieving score: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving score")
