## ATS Score Checker API Documentation

### Base URL
```
http://localhost:8000
```

### Health Check
Check if the API is running:
```bash
curl http://localhost:8000/api/health
```

Expected Response:
```json
{
    "status": "healthy"
}
```

### Upload Resume
Upload a resume file (PDF, DOCX, or TXT):
```bash
curl -X POST http://localhost:8000/api/v1/files/resume \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/resume.pdf"
```

Expected Response:
```json
{
    "file_id": "31a74553-f9e3-4742-8298-8c6e42e81bd8",
    "file_name": "resume.pdf",
    "file_type": "pdf",
    "file_size": 884,
    "uploaded_at": "2025-02-13T18:40:04.488543",
    "metadata": null
}
```

### Upload Job Description
Upload a job description file:
```bash
curl -X POST http://localhost:8000/api/v1/files/job \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/job.pdf" \
  -F "metadata={\"title\":\"Senior ML Engineer\",\"company\":\"AI Solutions Inc.\"}"
```

Expected Response:
```json
{
    "file_id": "bfd4708e-9e4a-46e2-860f-33da3f22c5f4",
    "file_name": "job.pdf",
    "file_type": "pdf",
    "file_size": 1401,
    "uploaded_at": "2025-02-13T18:40:04.495148",
    "metadata": {
        "title": "Senior ML Engineer",
        "company": "AI Solutions Inc."
    }
}
```

### Calculate Score
Calculate similarity scores between a resume and job description:
```bash
curl -X POST http://localhost:8000/api/v1/scores/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "31a74553-f9e3-4742-8298-8c6e42e81bd8",
    "job_id": "bfd4708e-9e4a-46e2-860f-33da3f22c5f4"
  }'
```

Expected Response:
```json
{
    "resume_id": "31a74553-f9e3-4742-8298-8c6e42e81bd8",
    "job_id": "bfd4708e-9e4a-46e2-860f-33da3f22c5f4",
    "tfidf_score": 32.57,
    "word2vec_score": 68.45,
    "sbert_score": 74.29,
    "combined_score": 57.60,
    "calculated_at": "2025-02-13T18:40:04.495148"
}
```

### List Resumes
Get a list of all uploaded resumes:
```bash
curl http://localhost:8000/api/v1/files/resumes
```

Expected Response:
```json
{
    "files": [
        {
            "file_id": "31a74553-f9e3-4742-8298-8c6e42e81bd8",
            "file_name": "resume.pdf",
            "file_type": "pdf",
            "file_size": 884,
            "uploaded_at": "2025-02-13T18:40:04.488543",
            "metadata": null
        }
    ],
    "total": 1
}
```

### List Jobs
Get a list of all uploaded job descriptions:
```bash
curl http://localhost:8000/api/v1/files/jobs
```

Expected Response:
```json
{
    "files": [
        {
            "file_id": "bfd4708e-9e4a-46e2-860f-33da3f22c5f4",
            "file_name": "job.pdf",
            "file_type": "pdf",
            "file_size": 1401,
            "uploaded_at": "2025-02-13T18:40:04.495148",
            "metadata": {
                "title": "Senior ML Engineer",
                "company": "AI Solutions Inc."
            }
        }
    ],
    "total": 1
}
```

### Delete File
Delete a file by ID:
```bash
curl -X DELETE http://localhost:8000/api/v1/files/31a74553-f9e3-4742-8298-8c6e42e81bd8
```

Expected Response:
```json
{
    "message": "File 31a74553-f9e3-4742-8298-8c6e42e81bd8 deleted successfully"
}
```

### Error Responses
The API returns appropriate error responses with details:

1. Invalid File Type:
```json
{
    "detail": "Invalid file type"
}
```

2. File Not Found:
```json
{
    "detail": "Resume with ID xxx not found"
}
```

3. Processing Error:
```json
{
    "detail": "Error processing resume"
}
``` 