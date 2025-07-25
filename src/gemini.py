import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def query_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY not found. Check your .env file.")
    print(GEMINI_API_KEY)

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.status_code}, {response.text}")

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
