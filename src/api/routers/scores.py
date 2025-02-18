"""
Score calculation endpoints.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

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
            word2vec_score=scores["word2vec_score"],
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


@router.get("/rankings", response_model=ScoreHistoryResponse)
async def get_rankings(
    job_id: Optional[str] = Query(None, description="Filter rankings by job ID")
) -> ScoreHistoryResponse:
    """
    Get rankings of all analyzed resumes, optionally filtered by job ID.
    """
    try:
        # In production, implement actual ranking retrieval from database
        # For now, return mock data
        scores = []
        if job_id:
            # Filter scores by job ID
            scores = [
                ScoreResponse(
                    resume_id=f"resume_{i}",
                    job_id=job_id,
                    tfidf_score=85.5 - i * 5,
                    word2vec_score=88.2 - i * 3,
                    sbert_score=90.1 - i * 4,
                    combined_score=88.3 - i * 4,
                    calculated_at=datetime.now(),
                )
                for i in range(5)  # Return 5 mock scores
            ]
        else:
            # Return all scores
            scores = [
                ScoreResponse(
                    resume_id=f"resume_{i}",
                    job_id=f"job_{i % 2 + 1}",
                    tfidf_score=85.5 - i * 5,
                    word2vec_score=88.2 - i * 3,
                    sbert_score=90.1 - i * 4,
                    combined_score=88.3 - i * 4,
                    calculated_at=datetime.now(),
                )
                for i in range(10)  # Return 10 mock scores
            ]

        # Sort scores by combined_score in descending order
        scores.sort(key=lambda x: x.combined_score, reverse=True)

        return ScoreHistoryResponse(scores=scores, total=len(scores))

    except Exception as e:
        logger.error(f"Error retrieving rankings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving rankings")


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
