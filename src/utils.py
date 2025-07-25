# src/utils.py
import json
import os

GROUND_TRUTH_FILE = os.path.join(os.path.dirname(__file__), "data", "mock_oura.json")

with open(GROUND_TRUTH_FILE, "r") as f:
    GROUND_TRUTH_DATA = json.load(f)

def find_ground_truth(timestamp_sec):
    for entry in GROUND_TRUTH_DATA:
        if entry.get("timestamp_sec") == timestamp_sec:
            return entry.get("sleep_stage", "Unknown")
    return "Unknown"
