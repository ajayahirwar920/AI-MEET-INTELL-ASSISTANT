#Parser Service
"""
Handles text extraction from:
1. txt files
2. pdf files
"""
from pathlib import Path
from pypdf import PdfReader

# Reading Text files
def read_txt(file_path: Path) -> str:
    """
    Read text from a TXT file or .txt file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    

# Reading PDF files
def read_pdf(file_path: Path) -> str:
    """
    Extract text from a PDF file using PyPdf2 from every page of a pdf.
    """
    
    reader = PdfReader(file_path)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        
        if page_text:
            text += page_text + "\n"
    
    return text


def extract_text(file_path: Path) -> str:
    """
    Extract text based on file extension. Supports .txt and .pdf files.
    """
    
    extension = file_path.suffix.lower()
    if extension == ".txt":
        return read_txt(file_path)
    
    elif extension == ".pdf":
        return read_pdf(file_path)
    
    else:
        raise ValueError(
            f"Unsupported file format or type: {extension}"
        )
        
    