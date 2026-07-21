# Speech Service
from faster_whisper import WhisperModel
# Load Model
model  = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    """
    Converts speech to text using the Faster Whisper model.
    Args:
        file_path (str): Path to the audio file.
    Returns:
        str: Transcribed text from the audio file.
    """
    
    segments, info = model.transcribe(file_path, beam_size=5)
    transcript = []
    for segment in segments:
        transcript.append(segment.text)
        
    return " ".join(transcript)
