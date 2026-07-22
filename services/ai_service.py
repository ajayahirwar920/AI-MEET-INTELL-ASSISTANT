import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Pass the API key here
client = genai.Client(api_key=API_KEY)

def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )
    return response.text
