import json
import re
from gemini import query_gemini
from utils import find_ground_truth

def extract_json_from_response(response: str) -> str:
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
    if match:
        return match.group(1)
    return response.strip()

def predict_sleep_stage(biometrics: dict):
    prompt = f"""
    You are a sleep science assistant helping personalize soundscapes during sleep.

Available sounds:
- white_noise.mp3: Neutral masking noise, good for light sleep
- pink_noise.mp3: Softer masking, better for deep sleep
- sleepy_rain.mp3: Gentle rain, promotes relaxation
- distant_breeze.mp3: Soft wind, ideal for REM sleep
- forest_atmosphere.mp3: Calming and grounding, good for transitions
- silence.mp3: No sound, use this if user needs silence

    Given the following biometric data, predict the current sleep stage (awake, light, deep, rem):
    Heart rate: {biometrics['heart_rate']}
    HRV: {biometrics['hrv']}
    Respiration rate: {biometrics['respiration_rate']}
    Movement score: {biometrics['movement_score']}
    Return JSON with keys: stage, sound, explanation.
    """

    raw_response = query_gemini(prompt)
    cleaned_response = extract_json_from_response(raw_response)

    try:
        result = json.loads(cleaned_response)
    except Exception as e:
        return {
            "stage": "Unknown",
            "sound": "silence.mp3",
            "explanation": f"Agent error: {str(e)}",
            "timestamp_sec": biometrics["timestamp_sec"],
            "ground_truth_stage": find_ground_truth(biometrics["timestamp_sec"])
        }

    result["timestamp_sec"] = biometrics["timestamp_sec"]
    result["ground_truth_stage"] = find_ground_truth(biometrics["timestamp_sec"])
    return result
