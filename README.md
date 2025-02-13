# ATS Score Checker

An intelligent system to evaluate resume compatibility with job descriptions using multiple similarity scoring methods.

## Project Overview
This project aims to create a reliable ATS (Applicant Tracking System) Score Checker that helps job seekers understand how well their resumes match with specific job descriptions. The system uses multiple advanced NLP techniques to provide comprehensive similarity scores.

## Features (Planned)
- Multiple similarity scoring methods:
  - TF-IDF + Cosine Similarity
  - Word2Vec Embeddings
  - SBERT (Sentence-BERT)
- Text preprocessing and cleaning
- Support for multiple file formats (PDF, DOCX, TXT)
- RESTful API interface
- Modern web interface (future phase)

## Project Structure
```
ATS-Score-Checker/
├── src/
│   ├── preprocessing/    # Text extraction and cleaning
│   ├── models/          # Similarity models implementation
│   └── api/             # FastAPI implementation
├── data/
│   ├── raw/            # Raw resume files
│   ├── processed/      # Processed text data
│   └── jobs/           # Job descriptions
├── notebooks/          # Jupyter notebooks for development
├── tests/             # Unit tests
├── docs/              # Documentation
└── venv/              # Virtual environment
```

## Setup
1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Status
Currently in Phase 1: Project Setup
- [x] Repository creation
- [x] Virtual environment setup
- [x] Project structure
- [x] Dependencies installation
- [x] Requirements.txt
- [x] README creation

## License
[MIT License](LICENSE)

## Contributing
This project is currently in its initial development phase. Contribution guidelines will be added in future phases.