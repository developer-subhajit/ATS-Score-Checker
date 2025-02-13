# ATS Score Checker

An intelligent system to evaluate resume compatibility with job descriptions using multiple similarity scoring methods.

## Overview
This tool helps job seekers understand how well their resumes match with specific job descriptions. It uses advanced NLP techniques to calculate similarity scores:

- TF-IDF with Cosine Similarity (40% weight)
- SBERT (Sentence-BERT) Embeddings (60% weight)

## Features
- Multiple similarity scoring methods
- Support for multiple file formats (PDF, DOCX, TXT)
- Text preprocessing and cleaning
- Intelligent scoring weights
- Caching for performance
- Comprehensive error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/developer-subhajit/ATS-Score-Checker.git
cd ATS-Score-Checker
```

2. Create and activate virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```python
from src.scoring_system import calculate_resume_match

# Calculate similarity scores between a JD and CV
scores = calculate_resume_match(
    jd_path="path/to/job_description.pdf",
    cv_path="path/to/resume.pdf"
)

print(scores)
# Output:
# {
#     'tfidf_score': 75.5,      # Keyword matching score (0-100)
#     'sbert_score': 82.3,      # Semantic similarity score (0-100)
#     'combined_score': 79.5    # Weighted final score (0-100)
# }
```

## Score Interpretation
- **TF-IDF Score**: Measures keyword matching and terminology alignment
- **SBERT Score**: Evaluates semantic similarity and contextual understanding
- **Combined Score**: Weighted average with SBERT (60%) and TF-IDF (40%)

Score ranges:
- 90-100: Excellent match
- 75-89: Good match
- 60-74: Moderate match
- Below 60: Poor match

## Project Structure
```
ATS-Score-Checker/
├── src/
│   ├── preprocessing/     # Text extraction and cleaning
│   │   ├── __init__.py
│   │   ├── data_manager.py
│   │   ├── file_handlers.py
│   │   └── text_processor.py
│   ├── models/           # Similarity models
│   │   ├── __init__.py
│   │   ├── base_similarity.py
│   │   ├── tfidf_similarity.py
│   │   └── sbert_similarity.py
│   ├── __init__.py
│   └── scoring_system.py # Main scoring logic
├── tests/               # Unit tests
│   ├── test_preprocessing.py
│   ├── test_similarity.py
│   └── test_scoring_system.py
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Adding New Similarity Methods
1. Create a new class in `src/models/` inheriting from `BaseSimilarity`
2. Implement required methods: `fit()`, `transform()`, `compute_similarity()`
3. Add the model to `ScoringSystem` class with appropriate weight

## License
[MIT License](LICENSE)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.