"""
File Service
---------------
Handle:
1. File Validation
2. File naming
3. Saving uploaded files 
"""

from pathlib import Path
from datetime import datetime
import os

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "mp3",
    "wav",
    "pdf",
    "mp4",
    "txt"
}

# Maximum upload size(2gb)
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  #2GB

# Upload Directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Validating File Extension
def allowed_file(filename:str) -> bool:
    """
    Check if the file has an allowed extension."""
    
    if "." not in filename:
        return False
    
    extension = filename.rsplit(".",1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

# Validate File Size
def validate_file(uploaded_file):
    """
    Validate the uploaded file for size.
    Returns:
    - True if the file is valid
    - False if the file is invalid
    """
    if not allowed_file(uploaded_file.name):
        return False, "❌ Unsupported file format or Type"
    
    if uploaded_file.size > MAX_FILE_SIZE:
        return False, "❌ File size exceeds the maximum limit of 2GB"
    
    return True, ""

# Unique File Name
def generate_filename(filename:str) -> str:
    """
    Generate a unique filename using timestamp.
    Example:
    meeting.mp3 -> 20262256_105262_meeting.mp3"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{filename}"


#Saving Uploaded files
def save_uploaded_file(uploaded_file) -> Path:
    """
    Save the uploaded file to uploads directory.
    Returns:
    Path to saved File.
    """
    filename = generate_filename(uploaded_file.name)
    file_path = UPLOAD_DIR / filename
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path

def delete_uploaded_file(file_path: Path):
    """
    Delete uploaded file after processing.
    """
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"Could not delete file:{e}")
    