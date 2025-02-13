"""
Tests for the API endpoints.
"""

import os

import pytest
from fastapi.testclient import TestClient

from src.api import app

# Initialize test client
client = TestClient(app)

# Test data paths
TEST_RESUME = "tests/sample_data/resumes/test_resume.txt"
TEST_JOB = "tests/sample_data/jobs/senior_ml_engineer.txt"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_upload_resume():
    """Test resume upload endpoint."""
    with open(TEST_RESUME, "rb") as f:
        response = client.post("/api/v1/files/resume", files={"file": ("test_resume.txt", f, "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["file_name"] == "test_resume.txt"
    assert data["file_type"] == "txt"


def test_upload_job():
    """Test job description upload endpoint."""
    with open(TEST_JOB, "rb") as f:
        response = client.post("/api/v1/files/job", files={"file": ("senior_ml_engineer.txt", f, "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["file_name"] == "senior_ml_engineer.txt"
    assert data["file_type"] == "txt"


def test_list_resumes():
    """Test resume listing endpoint."""
    response = client.get("/api/v1/files/resumes")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert "total" in data
    assert isinstance(data["files"], list)


def test_list_jobs():
    """Test job listing endpoint."""
    response = client.get("/api/v1/files/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert "total" in data
    assert isinstance(data["files"], list)


def test_calculate_score():
    """Test score calculation endpoint."""
    # First upload files
    with open(TEST_RESUME, "rb") as f:
        resume_response = client.post("/api/v1/files/resume", files={"file": ("test_resume.txt", f, "text/plain")})
    resume_id = resume_response.json()["file_id"]

    with open(TEST_JOB, "rb") as f:
        job_response = client.post("/api/v1/files/job", files={"file": ("senior_ml_engineer.txt", f, "text/plain")})
    job_id = job_response.json()["file_id"]

    # Calculate scores
    response = client.post("/api/v1/scores/calculate", json={"resume_id": resume_id, "job_id": job_id})
    assert response.status_code == 200
    data = response.json()
    assert "tfidf_score" in data
    assert "sbert_score" in data
    assert "combined_score" in data
    assert 0 <= data["tfidf_score"] <= 100
    assert 0 <= data["sbert_score"] <= 100
    assert 0 <= data["combined_score"] <= 100


def test_get_score_history():
    """Test score history endpoint."""
    response = client.get("/api/v1/scores/history")
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert "total" in data
    assert isinstance(data["scores"], list)


def test_invalid_file_type():
    """Test uploading invalid file type."""
    response = client.post(
        "/api/v1/files/resume", files={"file": ("test.xyz", b"invalid content", "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_missing_file():
    """Test uploading without file."""
    response = client.post("/api/v1/files/resume")
    assert response.status_code == 422  # Validation error


def test_invalid_score_request():
    """Test invalid score calculation request."""
    response = client.post("/api/v1/scores/calculate", json={"resume_id": "invalid", "job_id": "invalid"})
    assert response.status_code == 500  # File not found error


if __name__ == "__main__":
    pytest.main(["-v", __file__])
