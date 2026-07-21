# Speech Service
import streamlit as st
from faster_whisper import WhisperModel
# Load Model
@st.cache_resource
def load_whisper_model():
    """
    Load the Whisper model only once.
    Streamlit caches it across reruns.
    """
    return WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )


# Get the cached model
model = load_whisper_model()
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
