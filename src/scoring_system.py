"""
Scoring system that combines multiple similarity methods.
"""
import os
import json
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from functools import lru_cache
from .models import TFIDFSimilarity, SBERTSimilarity
from .preprocessing import DocumentReader, TextProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScoringSystem:
    """Combines multiple similarity methods to provide comprehensive scoring."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize the scoring system.
        
        Args:
            weights: Dictionary of weights for each method.
                    Default weights prioritize SBERT for semantic understanding.
                    
        Raises:
            ValueError: If weights are invalid or don't sum to 1
        """
        # Validate and set weights
        self._validate_and_set_weights(weights)
        
        # Initialize models
        self.models = {
            'tfidf': TFIDFSimilarity(),
            'sbert': SBERTSimilarity()
        }
        
        # Validate models match weights
        if not all(method in self.models for method in self.weights):
            raise ValueError("Weights specified for undefined methods")
        
        self.is_fitted = False
        self._cache = {}
    
    def _validate_and_set_weights(self, weights: Optional[Dict[str, float]]) -> None:
        """
        Validate and set scoring weights.
        
        Args:
            weights: Dictionary of weights for each method
            
        Raises:
            ValueError: If weights are invalid
        """
        # Default weights if none provided
        self.weights = weights or {
            'sbert': 0.6,  # SBERT gets highest weight for semantic understanding
            'tfidf': 0.4,  # TF-IDF for keyword matching
        }
        
        # Validate weights
        if not all(isinstance(w, (int, float)) for w in self.weights.values()):
            raise ValueError("All weights must be numeric")
        
        if any(w < 0 for w in self.weights.values()):
            raise ValueError("Weights cannot be negative")
        
        # Normalize weights to sum to 1
        total = sum(self.weights.values())
        if total == 0:
            raise ValueError("Weights cannot sum to zero")
            
        self.weights = {k: v/total for k, v in self.weights.items()}
    
    def _validate_text(self, text: str, name: str = "text") -> None:
        """
        Validate text input.
        
        Args:
            text: Text to validate
            name: Name of the text for error messages
            
        Raises:
            ValueError: If text is invalid
        """
        if text is None:
            raise ValueError(f"{name} cannot be None")
        if not isinstance(text, str):
            raise ValueError(f"{name} must be a string")
        if not text.strip():
            raise ValueError(f"{name} cannot be empty")
    
    @lru_cache(maxsize=1000)
    def _calculate_similarity_cached(self, resume: str, job_description: str) -> Dict[str, Any]:
        """Cached version of similarity calculation."""
        scores = {}
        weighted_sum = 0
        
        # Calculate individual scores
        for name, model in self.models.items():
            try:
                score_info = model.get_similarity_info(resume, job_description)
                scores[name] = {
                    'raw_score': score_info['raw_score'],
                    'normalized_score': score_info['normalized_score'],
                    'weight': self.weights[name]
                }
                weighted_sum += score_info['normalized_score'] * self.weights[name]
            except Exception as e:
                logger.error(f"Error calculating {name} score: {str(e)}")
                scores[name] = {'error': str(e)}
        
        # Add combined score
        scores['combined'] = {
            'score': weighted_sum,
            'weights_used': self.weights
        }
        
        return scores
    
    def fit_models(self, documents: List[str]) -> None:
        """
        Fit all similarity models.
        
        Args:
            documents: List of text documents
            
        Raises:
            ValueError: If documents are invalid
        """
        if not documents:
            raise ValueError("Document list cannot be empty")
            
        logger.info("Fitting models...")
        for name, model in self.models.items():
            logger.info(f"Fitting {name} model...")
            model.fit(documents)
        
        self.is_fitted = True
        self._cache.clear()  # Clear cache after fitting new data
    
    def calculate_similarity(self, resume: str, job_description: str) -> Dict[str, Any]:
        """
        Calculate similarity using all methods.
        
        Args:
            resume: Preprocessed resume text
            job_description: Preprocessed job description text
            
        Returns:
            Dictionary containing individual and combined scores
            
        Raises:
            ValueError: If inputs are invalid or models not fitted
        """
        # Validate inputs
        self._validate_text(resume, "Resume")
        self._validate_text(job_description, "Job description")
        
        if not self.is_fitted:
            raise ValueError("Models must be fitted before calculating similarity")
        
        return self._calculate_similarity_cached(resume, job_description)

def calculate_resume_match(jd_path: str, cv_path: str) -> Dict[str, float]:
    """
    Calculate similarity scores between a single JD and CV.
    
    Args:
        jd_path: Path to the job description file
        cv_path: Path to the CV/resume file
        
    Returns:
        Dictionary containing scores from each method
        
    Example:
        >>> scores = calculate_resume_match("job.pdf", "resume.pdf")
        >>> print(scores)
        {
            'tfidf_score': 75.5,
            'sbert_score': 82.3,
            'combined_score': 79.5
        }
    """
    try:
        # Initialize components
        doc_reader = DocumentReader()
        text_processor = TextProcessor()
        scorer = ScoringSystem()
        
        # Read and preprocess files
        jd_data = doc_reader.read_document(jd_path)
        cv_data = doc_reader.read_document(cv_path)
        
        jd_text = text_processor.preprocess_text(jd_data['text'])
        cv_text = text_processor.preprocess_text(cv_data['text'])
        
        # Fit models with both documents
        scorer.fit_models([jd_text, cv_text])
        
        # Calculate similarity
        scores = scorer.calculate_similarity(cv_text, jd_text)
        
        # Format output
        return {
            'tfidf_score': scores['tfidf']['normalized_score'],
            'sbert_score': scores['sbert']['normalized_score'],
            'combined_score': scores['combined']['score']
        }
        
    except Exception as e:
        logger.error(f"Error calculating scores: {str(e)}")
        raise 