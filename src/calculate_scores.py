"""
Script to calculate similarity scores between resumes and job descriptions.
"""
import os
import json
from typing import Dict, List, Any
import logging
from datetime import datetime
from preprocessing import DataManager, TextProcessor
from models import TFIDFSimilarity, SBERTSimilarity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScoreCalculator:
    """Calculates similarity scores between resumes and job descriptions."""
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize the score calculator.
        
        Args:
            data_dir: Base directory for data
        """
        self.data_manager = DataManager(data_dir)
        self.text_processor = TextProcessor()
        
        # Initialize similarity models
        self.models = {
            'tfidf': TFIDFSimilarity(),
            'sbert': SBERTSimilarity()
            # Word2Vec requires downloading a large model file
            # 'word2vec': Word2VecSimilarity()
        }
        
        # Create results directory
        self.results_dir = os.path.join(data_dir, 'results')
        os.makedirs(self.results_dir, exist_ok=True)
    
    def fit_models(self, documents: List[str]) -> None:
        """
        Fit all similarity models on the documents.
        
        Args:
            documents: List of all documents (resumes + job descriptions)
        """
        logger.info("Fitting similarity models...")
        for name, model in self.models.items():
            logger.info(f"Fitting {name} model...")
            model.fit(documents)
    
    def calculate_scores(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """
        Calculate similarity scores using all models.
        
        Args:
            resume_text: Preprocessed resume text
            job_text: Preprocessed job description text
            
        Returns:
            Dictionary containing scores from all models
        """
        scores = {}
        for name, model in self.models.items():
            try:
                score_info = model.get_similarity_info(resume_text, job_text)
                scores[name] = {
                    'raw_score': score_info['raw_score'],
                    'normalized_score': score_info['normalized_score']
                }
            except Exception as e:
                logger.error(f"Error calculating {name} score: {str(e)}")
                scores[name] = {'error': str(e)}
        return scores
    
    def process_documents(self) -> Dict[str, Any]:
        """
        Process all resumes and job descriptions and calculate scores.
        
        Returns:
            Dictionary containing all results
        """
        try:
            # Get all documents
            resumes = self.data_manager.get_processed_resumes()
            jobs = self.data_manager.get_job_descriptions()
            
            if not resumes:
                raise ValueError("No resumes found in the processed directory")
            if not jobs:
                raise ValueError("No job descriptions found in the jobs directory")
            
            # Combine all documents for fitting
            all_docs = [r['processed_text'] for r in resumes] + [j['processed_text'] for j in jobs]
            
            # Fit models
            self.fit_models(all_docs)
            
            # Calculate scores for each resume-job pair
            results = {
                'timestamp': datetime.now().isoformat(),
                'total_resumes': len(resumes),
                'total_jobs': len(jobs),
                'scores': []
            }
            
            for resume in resumes:
                resume_scores = []
                for job in jobs:
                    score_entry = {
                        'resume_file': resume['original_file'],
                        'job_title': job.get('job_title', 'Unknown'),
                        'job_file': job['original_file'],
                        'company': job.get('company', 'Unknown'),
                        'scores': self.calculate_scores(
                            resume['processed_text'],
                            job['processed_text']
                        )
                    }
                    resume_scores.append(score_entry)
                results['scores'].extend(resume_scores)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            raise
    
    def save_results(self, results: Dict[str, Any]) -> str:
        """
        Save results to a JSON file.
        
        Args:
            results: Dictionary containing all results
            
        Returns:
            Path to the saved results file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(self.results_dir, f'scores_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
        return output_file

def main():
    """Main execution function."""
    try:
        calculator = ScoreCalculator()
        results = calculator.process_documents()
        output_file = calculator.save_results(results)
        
        # Print summary
        print("\nProcessing Summary:")
        print(f"Total Resumes: {results['total_resumes']}")
        print(f"Total Jobs: {results['total_jobs']}")
        print(f"Total Comparisons: {len(results['scores'])}")
        print(f"\nResults saved to: {output_file}")
        
        # Print top matches
        print("\nTop Matches:")
        for score in sorted(
            results['scores'],
            key=lambda x: x['scores']['sbert']['normalized_score'],
            reverse=True
        )[:5]:
            print(f"\nResume: {score['resume_file']}")
            print(f"Job: {score['job_title']} at {score['company']}")
            print("Scores:")
            for model, model_scores in score['scores'].items():
                print(f"  {model}: {model_scores['normalized_score']:.2f}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == '__main__':
    main() 