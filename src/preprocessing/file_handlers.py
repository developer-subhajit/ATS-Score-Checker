"""
File handlers for different document types (PDF, DOCX, TXT).
"""
import os
from typing import Dict, Any
import fitz  # PyMuPDF
from docx import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentReader:
    """Handles reading different document formats."""
    
    @staticmethod
    def read_pdf(file_path: str) -> str:
        """Extract text from PDF files using PyMuPDF."""
        try:
            with fitz.open(file_path) as pdf_doc:
                text = ""
                for page in pdf_doc:
                    text += page.get_text()
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def read_docx(file_path: str) -> str:
        """Extract text from DOCX files using python-docx."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading DOCX file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def read_txt(file_path: str) -> str:
        """Read text from TXT files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Error reading TXT file {file_path}: {str(e)}")
            raise
    
    def read_document(self, file_path: str) -> Dict[str, Any]:
        """
        Read any supported document format and return its content with metadata.
        
        Returns:
            Dict containing:
            - text: extracted text content
            - file_name: original file name
            - file_type: document type (pdf, docx, txt)
            - file_size: size in bytes
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_ext = file_name.lower().split('.')[-1]
        
        try:
            if file_ext == 'pdf':
                text = self.read_pdf(file_path)
                doc_type = 'pdf'
            elif file_ext == 'docx':
                text = self.read_docx(file_path)
                doc_type = 'docx'
            elif file_ext == 'txt':
                text = self.read_txt(file_path)
                doc_type = 'txt'
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            return {
                'text': text,
                'file_name': file_name,
                'file_type': doc_type,
                'file_size': file_size
            }
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise 