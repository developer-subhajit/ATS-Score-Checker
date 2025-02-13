#!/usr/bin/env python3
"""
Download required NLTK data.
"""
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download required NLTK data packages."""
    required_packages = [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger'
    ]
    
    for package in required_packages:
        print(f"Downloading {package}...")
        nltk.download(package, quiet=True)
    
    print("All NLTK packages downloaded successfully!")

if __name__ == '__main__':
    download_nltk_data() 