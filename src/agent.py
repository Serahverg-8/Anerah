import json
from gemini import query_gemini

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "sleep_history.json")) as f:
    sleep_history = json.load(f)

with open(os.path.join(BASE_DIR, "data", "mock_oura.json")) as f:
    biometric_data = json.load(f)

def predict_sleep_stage(hour, mood=None):
    if hour >= len(biometric_data):
        return {
            "stage": "Wake",
            "sound": "white_noise.mp3",
            "explanation": "User is assumed to be awake after end of sleep cycle."
        }

    current_bio = biometric_data[hour]

    prompt = f"""
You are a sleep agent optimizing soundscapes for restful sleep.

The user has the following sleep history over the past 5 nights:
{json.dumps(sleep_history, indent=2)}

It is now hour {hour} into sleep. Current biometrics are:
- Heart Rate: {current_bio['heart_rate']} bpm
- HRV: {current_bio['hrv']}
- Movement Index: {current_bio['movement']}

{"The user went to sleep feeling " + mood + "." if mood else ""}

Please respond with concise, valid JSON only, without any extra commentary.

Return a JSON object in this format:
{{
  "stage": "REM",
  "sound": "distant_breeze.mp3",
  "explanation": "HRV and stillness suggest REM sleep."
}}
"""

    try:
        response = query_gemini(prompt)
        print("Raw Gemini response:", repr(response))  # Debug print

        # Remove markdown code fences if present
        if response.startswith("```json"):
            response = response.partition("\n")[2]  # Remove first line ```json
            if response.endswith("```"):
                response = response[:-3]  # Remove last line ```
            response = response.strip()

        return json.loads(response)
    except json.JSONDecodeError:
        # Try to auto-fix truncated JSON by adding a closing brace
        fixed_response = response.strip()
        if not fixed_response.endswith('}'):
            fixed_response += "}"
        return json.loads(fixed_response)
    except Exception as e:
        return {
            "stage": "Unknown",
            "sound": "silence.mp3",
            "explanation": f"Agent error: {str(e)}"
        }
