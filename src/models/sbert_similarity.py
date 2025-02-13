"""
SBERT (Sentence-BERT) based similarity scoring.
"""
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .base_similarity import BaseSimilarity


class SBERTSimilarity(BaseSimilarity):
    """Computes similarity using SBERT embeddings."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize SBERT similarity scorer.
        
        Args:
            model_name: Name of the pre-trained SBERT model to use.
                       Defaults to all-MiniLM-L6-v2 which provides a good
                       balance between performance and speed.
        """
        super().__init__()
        self.model_name = model_name
        self.model = None
        
    def fit(self, documents: List[str]) -> None:
        """
        Load the SBERT model.
        
        Args:
            documents: List of documents (not used for pre-trained model)
        """
        self.model = SentenceTransformer(self.model_name)
        self.is_fitted = True
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform documents into SBERT embeddings.
        
        Args:
            documents: List of text documents to transform
            
        Returns:
            Array of document embeddings
        """
        if not self.is_fitted:
            raise ValueError("Model must be loaded before transform")
            
        # Encode documents to get embeddings
        embeddings = self.model.encode(
            documents,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def compute_similarity(self, resume: str, job_description: str) -> float:
        """
        Compute cosine similarity between resume and job description embeddings.
        
        Args:
            resume: Preprocessed resume text
            job_description: Preprocessed job description text
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        # Get document embeddings
        embeddings = self.transform([resume, job_description])
        
        # Compute cosine similarity
        similarity = cosine_similarity(
            embeddings[0].reshape(1, -1),
            embeddings[1].reshape(1, -1)
        )
        
        return float(similarity[0, 0]) 