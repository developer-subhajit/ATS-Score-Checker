"""
Base class for similarity scoring methods.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import numpy as np


class BaseSimilarity(ABC):
    """Abstract base class for all similarity scoring methods."""
    
    def __init__(self):
        """Initialize the similarity scorer."""
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, documents: List[str]) -> None:
        """
        Fit the model on a list of documents.
        
        Args:
            documents: List of text documents to fit the model on
        """
        pass
    
    @abstractmethod
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform documents into vector representations.
        
        Args:
            documents: List of text documents to transform
            
        Returns:
            Array of vector representations
        """
        pass
    
    def fit_transform(self, documents: List[str]) -> np.ndarray:
        """
        Fit the model and transform documents in one step.
        
        Args:
            documents: List of text documents to fit and transform
            
        Returns:
            Array of vector representations
        """
        self.fit(documents)
        return self.transform(documents)
    
    @abstractmethod
    def compute_similarity(self, resume: str, job_description: str) -> float:
        """
        Compute similarity score between a resume and job description.
        
        Args:
            resume: Preprocessed resume text
            job_description: Preprocessed job description text
            
        Returns:
            Similarity score between 0 and 1
        """
        pass
    
    def normalize_score(self, score: float) -> float:
        """
        Normalize similarity score to be between 0 and 100.
        
        Args:
            score: Raw similarity score
            
        Returns:
            Normalized score between 0 and 100
        """
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, score))
        # Convert to percentage
        return score * 100
    
    def get_similarity_info(self, resume: str, job_description: str) -> Dict[str, Any]:
        """
        Get detailed similarity information between resume and job description.
        
        Args:
            resume: Preprocessed resume text
            job_description: Preprocessed job description text
            
        Returns:
            Dictionary containing:
            - raw_score: Original similarity score
            - normalized_score: Score between 0-100
            - method: Name of similarity method used
        """
        raw_score = self.compute_similarity(resume, job_description)
        return {
            'raw_score': raw_score,
            'normalized_score': self.normalize_score(raw_score),
            'method': self.__class__.__name__
        } 