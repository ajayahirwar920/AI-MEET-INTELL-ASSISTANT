# Parser Service
# Responsible for extracting text from supported file

from pathlib import Path
from pypdf import PdfReader


# Read TXT File
def read_txt(file_path: Path) -> str:
    """
    Reads a txt from .txt file.
    Args:
        file_path (Path): Path to the txt file.
    
    Returns:
        Text content as a string.
    """
    
    with open(file_path, "r", encoding = "utf-8") as file:
        return file.read()
    

# Read PDF File
def read_pdf(file_path: Path) -> str:
    """
    Extracts text from a PDf file of every page.
    """
    reader = PdfReader(file_path)
    extracted_text = []
    for page in reader.pages:
        text = page.extract_text()
        
        if text:
            extracted_text.append(text)
            
    return "\n".join(extracted_text)


# Dispatcher
def extract_text(file_path: Path) -> str:
    """
    Determines the file type adn extracts text accordingly.
    """
    
    extensions = file_path.suffix.lower()
    
    parser = {
        ".txt": read_txt,
        ".pdf": read_pdf
    }
    
    parser = parsers.get(extension)
    
    if parser is None:
        raise ValueError(
            f"Unsupported file type: {extension}"
    )
    
    return parser(file_path)