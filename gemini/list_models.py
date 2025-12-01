import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

print("Listing available models for this API key:\n")
for m in genai.list_models():
    # m.name is like "models/gemini-1.5-flash"
    print(m.name, "->", m.supported_generation_methods)
