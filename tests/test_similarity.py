"""
Tests for similarity scoring models.
"""
import pytest
import numpy as np
from src.models import TFIDFSimilarity, Word2VecSimilarity, SBERTSimilarity

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
def sample_documents():
    return [SAMPLE_RESUME, SAMPLE_JOB, UNRELATED_TEXT]

@pytest.fixture
def fitted_tfidf_model(sample_documents):
    model = TFIDFSimilarity()
    model.fit(sample_documents)
    return model

@pytest.fixture
def word2vec_model():
    return Word2VecSimilarity()

@pytest.fixture
def fitted_sbert_model(sample_documents):
    model = SBERTSimilarity()
    model.fit(sample_documents)
    return model

class TestTFIDFSimilarity:
    def test_initialization(self, fitted_tfidf_model):
        assert hasattr(fitted_tfidf_model, 'vectorizer')
        assert fitted_tfidf_model.is_fitted

    def test_fit_transform(self, fitted_tfidf_model, sample_documents):
        vectors = fitted_tfidf_model.transform(sample_documents)
        assert isinstance(vectors, np.ndarray)
        assert vectors.shape[0] == len(sample_documents)

    def test_similarity_score_range(self, fitted_tfidf_model):
        score = fitted_tfidf_model.compute_similarity(SAMPLE_RESUME, SAMPLE_JOB)
        assert 0 <= score <= 1

    def test_similar_docs_higher_score(self, fitted_tfidf_model):
        similar_score = fitted_tfidf_model.compute_similarity(SAMPLE_RESUME, SAMPLE_JOB)
        different_score = fitted_tfidf_model.compute_similarity(SAMPLE_RESUME, UNRELATED_TEXT)
        assert similar_score > different_score

class TestWord2VecSimilarity:
    def test_initialization(self, word2vec_model):
        assert not word2vec_model.is_fitted
        assert word2vec_model.word_vectors is None

    @pytest.mark.skip(reason="Requires downloading large model file")
    def test_fit_transform(self, word2vec_model, sample_documents):
        vectors = word2vec_model.fit_transform(sample_documents)
        assert word2vec_model.is_fitted
        assert isinstance(vectors, np.ndarray)
        assert vectors.shape[0] == len(sample_documents)

    def test_transform_without_fit(self, word2vec_model, sample_documents):
        with pytest.raises(ValueError):
            word2vec_model.transform(sample_documents)

class TestSBERTSimilarity:
    def test_initialization(self, fitted_sbert_model):
        assert fitted_sbert_model.is_fitted
        assert fitted_sbert_model.model is not None

    def test_fit_transform(self, fitted_sbert_model, sample_documents):
        vectors = fitted_sbert_model.transform(sample_documents)
        assert isinstance(vectors, np.ndarray)
        assert vectors.shape[0] == len(sample_documents)

    def test_similarity_score_range(self, fitted_sbert_model):
        score = fitted_sbert_model.compute_similarity(SAMPLE_RESUME, SAMPLE_JOB)
        assert 0 <= score <= 1

    def test_similar_docs_higher_score(self, fitted_sbert_model):
        similar_score = fitted_sbert_model.compute_similarity(SAMPLE_RESUME, SAMPLE_JOB)
        different_score = fitted_sbert_model.compute_similarity(SAMPLE_RESUME, UNRELATED_TEXT)
        assert similar_score > different_score

def test_normalized_scores(fitted_tfidf_model, fitted_sbert_model):
    """Test that all models return normalized scores between 0 and 100"""
    models = [
        fitted_tfidf_model,
        fitted_sbert_model
    ]
    
    for model in models:
        info = model.get_similarity_info(SAMPLE_RESUME, SAMPLE_JOB)
        assert 0 <= info['raw_score'] <= 1
        assert 0 <= info['normalized_score'] <= 100
        assert isinstance(info['method'], str) 