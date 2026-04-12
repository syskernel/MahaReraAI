from google import genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def contact_info(name, location, project):
    prompt = f"""
        Find only the phone numbers for {name} located at {location} for the project {project}.

        Rules:
        - Output ONLY phone numbers
        - One number per line
        - No text, no labels, no explanation
        - Remove country code if present (keep 10 digits only)

        Example output:
        9935357272
        8044566852
        """
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview", contents=prompt
    )

    data = response.text.strip()
    numbers = re.findall(r'\+?\d[\d\s\-]{8,}\d', data)
    clean_numbers = [re.sub(r'\D', '', num)[-10:] for num in numbers]
    
    return clean_numbers