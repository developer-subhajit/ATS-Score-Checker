"""
TF-IDF based similarity scoring.
"""
from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .base_similarity import BaseSimilarity


class TFIDFSimilarity(BaseSimilarity):
    """Computes similarity using TF-IDF vectors and cosine similarity."""
    
    def __init__(self, max_features: Optional[int] = None, 
                 ngram_range: tuple = (1, 1)):
        """
        Initialize TF-IDF similarity scorer.
        
        Args:
            max_features: Maximum number of features to use
            ngram_range: The lower and upper boundary of the range of n-values for 
                        different n-grams to be extracted
        """
        super().__init__()
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range
        )
    
    def fit(self, documents: List[str]) -> None:
        """
        Fit TF-IDF vectorizer on a list of documents.
        
        Args:
            documents: List of text documents to fit the vectorizer on
        """
        self.vectorizer.fit(documents)
        self.is_fitted = True
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform documents into TF-IDF vectors.
        
        Args:
            documents: List of text documents to transform
            
        Returns:
            Array of TF-IDF vectors
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer must be fitted before transform")
        return self.vectorizer.transform(documents).toarray()
    
    def compute_similarity(self, resume: str, job_description: str) -> float:
        """
        Compute cosine similarity between resume and job description TF-IDF vectors.
        
        Args:
            resume: Preprocessed resume text
            job_description: Preprocessed job description text
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        # Transform both texts
        vectors = self.transform([resume, job_description])
        
        # Compute cosine similarity
        similarity = cosine_similarity(
            vectors[0].reshape(1, -1),
            vectors[1].reshape(1, -1)
        )
        
        return float(similarity[0, 0]) 