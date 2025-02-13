"""
Tests for the scoring system.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from src.scoring_system import ScoringSystem, calculate_resume_match

# Sample test data
SAMPLE_RESUME = """
Python developer with 5 years experience in machine learning and data science.
Proficient in scikit-learn, TensorFlow, and PyTorch.
"""

SAMPLE_JOB = """
Looking for a Python developer with machine learning experience.
Must know scikit-learn and deep learning frameworks.
"""

UNRELATED_TEXT = """
Experienced chef with 10 years in Italian cuisine.
Specializes in pasta and pizza making.
"""

@pytest.fixture
def scorer():
    """Initialize scoring system with default weights."""
    return ScoringSystem()

@pytest.fixture
def custom_weighted_scorer():
    """Initialize scoring system with custom weights."""
    weights = {
        'sbert': 0.7,
        'tfidf': 0.3
    }
    return ScoringSystem(weights=weights)

def test_initialization(scorer):
    """Test scoring system initialization."""
    assert scorer.weights['sbert'] == 0.6
    assert scorer.weights['tfidf'] == 0.4
    assert sum(scorer.weights.values()) == 1.0

def test_custom_weights(custom_weighted_scorer):
    """Test custom weight initialization."""
    assert custom_weighted_scorer.weights['sbert'] == 0.7
    assert custom_weighted_scorer.weights['tfidf'] == 0.3
    assert sum(custom_weighted_scorer.weights.values()) == 1.0

def test_invalid_weights():
    """Test invalid weight configurations."""
    with pytest.raises(ValueError):
        ScoringSystem(weights={'invalid_method': 1.0})

def test_calculate_similarity(scorer):
    """Test similarity calculation."""
    # Fit models first
    scorer.fit_models([SAMPLE_RESUME, SAMPLE_JOB])
    
    # Calculate scores
    scores = scorer.calculate_similarity(SAMPLE_RESUME, SAMPLE_JOB)
    
    # Check structure
    assert 'tfidf' in scores
    assert 'sbert' in scores
    assert 'combined' in scores
    
    # Check score ranges
    for method, details in scores.items():
        if method != 'combined':
            assert 0 <= details['raw_score'] <= 1
            assert 0 <= details['normalized_score'] <= 100
            assert details['weight'] > 0
    
    assert 0 <= scores['combined']['score'] <= 100

def test_error_handling(scorer):
    """Test error handling in scoring system."""
    # Test with empty text
    with pytest.raises(ValueError):
        scorer.calculate_similarity("", SAMPLE_JOB)
    
    # Test with None
    with pytest.raises(ValueError):
        scorer.calculate_similarity(None, SAMPLE_JOB)
    
    # Test without fitting
    with pytest.raises(ValueError):
        scorer.calculate_similarity(SAMPLE_RESUME, SAMPLE_JOB)
    
    # Test with empty document list for fitting
    with pytest.raises(ValueError):
        scorer.fit_models([])

def test_calculate_resume_match(tmp_path):
    """Test the simplified JD-CV matching function."""
    # Create temporary test files
    jd_file = tmp_path / "test_jd.txt"
    cv_file = tmp_path / "test_cv.txt"
    
    # Write test content
    jd_file.write_text(SAMPLE_JOB)
    cv_file.write_text(SAMPLE_RESUME)
    
    # Calculate scores
    scores = calculate_resume_match(str(jd_file), str(cv_file))
    
    # Check structure
    assert 'tfidf_score' in scores
    assert 'sbert_score' in scores
    assert 'combined_score' in scores
    
    # Check score ranges
    assert 0 <= scores['tfidf_score'] <= 100
    assert 0 <= scores['sbert_score'] <= 100
    assert 0 <= scores['combined_score'] <= 100
    
    # Test with unrelated CV
    unrelated_cv = tmp_path / "unrelated_cv.txt"
    unrelated_cv.write_text(UNRELATED_TEXT)
    
    unrelated_scores = calculate_resume_match(str(jd_file), str(unrelated_cv))
    
    # Unrelated CV should have lower scores
    assert unrelated_scores['combined_score'] < scores['combined_score'] 