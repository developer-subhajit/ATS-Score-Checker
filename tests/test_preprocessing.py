"""
Unit tests for the preprocessing pipeline.
"""
import os
import json
import unittest
from src.preprocessing import DocumentReader, TextProcessor, DataManager

class TestPreprocessing(unittest.TestCase):
    """Test cases for preprocessing pipeline."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data and paths."""
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        cls.sample_resume = os.path.join(cls.base_dir, 'sample_data/resumes/test_resume.txt')
        cls.sample_job = os.path.join(cls.base_dir, 'sample_data/jobs/senior_ml_engineer.txt')
        
        # Initialize processors
        cls.doc_reader = DocumentReader()
        cls.text_processor = TextProcessor()
        cls.data_manager = DataManager(base_dir='tests/data')
    
    def test_document_reader(self):
        """Test document reading functionality."""
        # Test resume reading
        resume_data = self.doc_reader.read_document(self.sample_resume)
        self.assertIsInstance(resume_data, dict)
        self.assertIn('text', resume_data)
        self.assertIn('file_name', resume_data)
        self.assertEqual(resume_data['file_type'], 'txt')
        
        # Test job description reading
        job_data = self.doc_reader.read_document(self.sample_job)
        self.assertIsInstance(job_data, dict)
        self.assertIn('text', job_data)
        self.assertIn('file_name', job_data)
        self.assertEqual(job_data['file_type'], 'txt')
    
    def test_text_processor(self):
        """Test text processing functionality."""
        sample_text = "This is a TEST email: test@email.com with some Numbers: 12345"
        
        # Test text cleaning
        cleaned_text = self.text_processor.clean_text(sample_text)
        self.assertNotIn('@', cleaned_text)
        self.assertNotIn('12345', cleaned_text)
        self.assertEqual(cleaned_text, cleaned_text.lower())
        
        # Test stopword removal
        text_without_stopwords = self.text_processor.remove_stopwords(cleaned_text)
        self.assertNotIn(' is ', f' {text_without_stopwords} ')
        self.assertNotIn(' a ', f' {text_without_stopwords} ')
        
        # Test full preprocessing
        processed_text = self.text_processor.preprocess_text(sample_text)
        self.assertTrue(len(processed_text) < len(sample_text))
    
    def test_data_manager(self):
        """Test data management functionality."""
        # Test resume processing
        resume_result = self.data_manager.save_resume(self.sample_resume)
        self.assertIsInstance(resume_result, dict)
        self.assertIn('processed_text', resume_result)
        self.assertIn('raw_text', resume_result)
        
        # Test job description processing
        job_result = self.data_manager.save_job_description(
            self.sample_job,
            job_title="Senior ML Engineer"
        )
        self.assertIsInstance(job_result, dict)
        self.assertIn('processed_text', job_result)
        self.assertIn('raw_text', job_result)
        self.assertEqual(job_result['job_title'], "Senior ML Engineer")
        
        # Test getting processed documents
        resumes = self.data_manager.get_processed_resumes()
        self.assertIsInstance(resumes, list)
        self.assertTrue(len(resumes) > 0)
        
        jobs = self.data_manager.get_job_descriptions()
        self.assertIsInstance(jobs, list)
        self.assertTrue(len(jobs) > 0)
    
    def test_end_to_end_processing(self):
        """Test the entire preprocessing pipeline."""
        # Process resume
        resume_data = self.doc_reader.read_document(self.sample_resume)
        processed_resume = self.text_processor.preprocess_text(resume_data['text'])
        
        # Verify resume processing
        self.assertIn('python', processed_resume.lower())
        self.assertIn('machine', processed_resume.lower())
        self.assertIn('learning', processed_resume.lower())
        self.assertNotIn('email:', processed_resume.lower())
        self.assertNotIn('@', processed_resume)
        
        # Process job description
        job_data = self.doc_reader.read_document(self.sample_job)
        processed_job = self.text_processor.preprocess_text(job_data['text'])
        
        # Verify job processing
        self.assertIn('python', processed_job.lower())
        self.assertIn('machine', processed_job.lower())
        self.assertIn('learning', processed_job.lower())
        self.assertNotIn('email:', processed_job.lower())
        self.assertNotIn('@', processed_job)

if __name__ == '__main__':
    unittest.main() 