"""
Text preprocessing utilities for cleaning and normalizing text data.
"""
import re
from typing import List, Optional
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    logger.error(f"Error downloading NLTK data: {str(e)}")
    raise

class TextProcessor:
    """Handles text preprocessing and normalization."""
    
    def __init__(self, language: str = 'english'):
        """
        Initialize the text processor.
        
        Args:
            language: Language for stopwords (default: 'english')
        """
        self.language = language
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
        self.word_tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters and extra whitespace.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove email addresses and URLs
        text = re.sub(r'\S+@\S+|http\S+|www.\S+', ' ', text)
        
        # Replace bullet points and list markers with periods
        text = re.sub(r'[\u2022\-\*]\s*', '. ', text)
        
        # Replace multiple newlines with periods
        text = re.sub(r'\n+', '. ', text)
        
        # Remove other special characters and numbers
        text = re.sub(r'[^a-zA-Z\s\.]', ' ', text)
        
        # Normalize spaces around periods
        text = re.sub(r'\s*\.\s*', '. ', text)
        
        # Clean up multiple spaces and periods
        text = re.sub(r'\.+', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Split into sentences and filter empty ones
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        return '. '.join(sentences)
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from text.
        
        Args:
            text: Input text
            
        Returns:
            Text with stopwords removed
        """
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Process each sentence
        processed_sentences = []
        for sentence in sentences:
            words = self.word_tokenizer.tokenize(sentence)
            filtered_words = [word for word in words if word.lower() not in self.stop_words]
            if filtered_words:  # Only add non-empty sentences
                processed_sentences.append(' '.join(filtered_words))
        
        return '. '.join(processed_sentences)
    
    def lemmatize_text(self, text: str) -> str:
        """
        Lemmatize text to get base word forms.
        
        Args:
            text: Input text
            
        Returns:
            Lemmatized text
        """
        words = self.word_tokenizer.tokenize(text)
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)
    
    def preprocess_text(self, text: str, remove_stopwords: bool = True, 
                       lemmatize: bool = True) -> str:
        """
        Apply full preprocessing pipeline to text.
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stopwords
            lemmatize: Whether to apply lemmatization
            
        Returns:
            Preprocessed text
        """
        try:
            # Clean text
            text = self.clean_text(text)
            
            # Remove stopwords if requested
            if remove_stopwords:
                text = self.remove_stopwords(text)
            
            # Lemmatize if requested
            if lemmatize:
                text = self.lemmatize_text(text)
            
            return text
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            raise 