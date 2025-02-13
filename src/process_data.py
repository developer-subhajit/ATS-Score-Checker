"""
Script to process resumes and job descriptions.
"""
import os
import argparse
from preprocessing import DataManager

def process_files(resume_dir: str = None, job_dir: str = None):
    """
    Process resume and job description files.
    
    Args:
        resume_dir: Directory containing resume files
        job_dir: Directory containing job description files
    """
    data_manager = DataManager()
    
    # Process resumes
    if resume_dir and os.path.exists(resume_dir):
        print(f"\nProcessing resumes from: {resume_dir}")
        for file in os.listdir(resume_dir):
            file_path = os.path.join(resume_dir, file)
            if os.path.isfile(file_path):
                try:
                    result = data_manager.save_resume(file_path)
                    print(f"✓ Processed resume: {file}")
                except Exception as e:
                    print(f"✗ Error processing resume {file}: {str(e)}")
    
    # Process job descriptions
    if job_dir and os.path.exists(job_dir):
        print(f"\nProcessing job descriptions from: {job_dir}")
        for file in os.listdir(job_dir):
            file_path = os.path.join(job_dir, file)
            if os.path.isfile(file_path):
                try:
                    # Extract job title from filename (you might want to modify this)
                    job_title = os.path.splitext(file)[0].replace('_', ' ').title()
                    result = data_manager.save_job_description(
                        file_path,
                        job_title=job_title
                    )
                    print(f"✓ Processed job description: {file}")
                except Exception as e:
                    print(f"✗ Error processing job description {file}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Process resumes and job descriptions')
    parser.add_argument('--resumes', help='Directory containing resume files')
    parser.add_argument('--jobs', help='Directory containing job description files')
    
    args = parser.parse_args()
    
    if not args.resumes and not args.jobs:
        parser.print_help()
        return
    
    process_files(args.resumes, args.jobs)
    print("\nProcessing complete!")

if __name__ == '__main__':
    main() 