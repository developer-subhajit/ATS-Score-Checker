"""
Word2Vec based similarity scoring.
"""
from typing import List, Optional
import numpy as np
from gensim.models import KeyedVectors
from .base_similarity import BaseSimilarity


class Word2VecSimilarity(BaseSimilarity):
    """Computes similarity using Word2Vec embeddings."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize Word2Vec similarity scorer.
        
        Args:
            model_path: Path to pre-trained Word2Vec model in binary format.
                       If None, will use a default model.
        """
        super().__init__()
        self.model_path = model_path
        self.word_vectors = None
        
    def fit(self, documents: List[str]) -> None:
        """
        Load the Word2Vec model.
        
        Args:
            documents: List of documents (not used for pre-trained model)
        """
        if self.model_path:
            self.word_vectors = KeyedVectors.load_word2vec_format(
                self.model_path, 
                binary=True
            )
        else:
            # Load default model
            self.word_vectors = KeyedVectors.load_word2vec_format(
                'models/GoogleNews-vectors-negative300.bin',
                binary=True
            )
        self.is_fitted = True
    
    def _get_document_vector(self, text: str) -> np.ndarray:
        """
        Convert document to vector by averaging word vectors.
        
        Args:
            text: Input text document
            
        Returns:
            Document vector as numpy array
        """
        words = text.split()
        vectors = []
        
        for word in words:
            try:
                vector = self.word_vectors[word]
                vectors.append(vector)
            except KeyError:
                continue
                
        if not vectors:
            return np.zeros(self.word_vectors.vector_size)
            
        return np.mean(vectors, axis=0)
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform documents into document vectors.
        
        Args:
            documents: List of text documents to transform
            
        Returns:
            Array of document vectors
        """
        if not self.is_fitted:
            raise ValueError("Model must be loaded before transform")
            
        vectors = []
        for doc in documents:
            vec = self._get_document_vector(doc)
            vectors.append(vec)
            
        return np.array(vectors)
    
    def compute_similarity(self, resume: str, job_description: str) -> float:
        """
        Compute cosine similarity between resume and job description vectors.
        
        Args:
            resume: Preprocessed resume text
            job_description: Preprocessed job description text
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        # Get document vectors
        resume_vec = self._get_document_vector(resume)
        jd_vec = self._get_document_vector(job_description)
        
        # Compute cosine similarity
        similarity = np.dot(resume_vec, jd_vec) / (
            np.linalg.norm(resume_vec) * np.linalg.norm(jd_vec)
        )
        
        return float(similarity) 