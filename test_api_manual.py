"""
Manual API testing script.
"""

import json

import requests

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check endpoint."""
    response = requests.get(f"{BASE_URL}/api/health")
    print("\nHealth Check Response:", response.json())
    return response.status_code == 200


def test_upload_resume():
    """Test resume upload."""
    files = {"file": ("test_resume.txt", open("tests/sample_data/resumes/test_resume.txt", "rb"), "text/plain")}
    response = requests.post(f"{BASE_URL}/api/v1/files/resume", files=files)
    print("\nResume Upload Response:", response.json())
    return response.status_code == 200, response.json().get("file_id")


def test_upload_job():
    """Test job description upload."""
    files = {
        "file": ("senior_ml_engineer.txt", open("tests/sample_data/jobs/senior_ml_engineer.txt", "rb"), "text/plain")
    }
    response = requests.post(f"{BASE_URL}/api/v1/files/job", files=files)
    print("\nJob Upload Response:", response.json())
    return response.status_code == 200, response.json().get("file_id")


def test_calculate_score(resume_id: str, job_id: str):
    """Test score calculation."""
    data = {"resume_id": resume_id, "job_id": job_id}
    response = requests.post(f"{BASE_URL}/api/v1/scores/calculate", json=data)
    print("\nScore Calculation Response:", response.json())
    return response.status_code == 200


def main():
    """Run all tests."""
    print("Testing API endpoints...")

    # Test health check
    if test_health():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")

    # Test resume upload
    resume_success, resume_id = test_upload_resume()
    if resume_success:
        print("✅ Resume upload passed")
    else:
        print("❌ Resume upload failed")

    # Test job upload
    job_success, job_id = test_upload_job()
    if job_success:
        print("✅ Job upload passed")
    else:
        print("❌ Job upload failed")

    # Test score calculation
    if resume_success and job_success:
        if test_calculate_score(resume_id, job_id):
            print("✅ Score calculation passed")
        else:
            print("❌ Score calculation failed")
    else:
        print("⚠️ Skipping score calculation due to upload failures")


if __name__ == "__main__":
    main()
