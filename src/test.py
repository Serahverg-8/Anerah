import sys
sys.path.append("src")
from agent import predict_sleep_stage

print(predict_sleep_stage(1, mood="tired"))


#generate historic data scaled down to 90 sec
import json
from datetime import datetime, timedelta
import random

def generate_realistic_sleep_history(days=5):
    sleep_history = []
    for i in range(days):
        sleep_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')

        total_duration = random.randint(360, 510)  # 6 to 8.5 hours in minutes

        awake = random.randint(10, 25)
        deep = random.randint(45, 100)
        rem = random.randint(60, 110)
        light = total_duration - (awake + deep + rem)

        avg_hr = random.randint(53, 72)
        avg_hrv = random.randint(35, 75)
        respiration = round(random.uniform(11.0, 18.5), 1)
        movement = round(random.uniform(0.15, 0.6), 2)

        sleep_entry = {
            "date": sleep_date,
            "duration_minutes": total_duration,
            "avg_heart_rate": avg_hr,
            "avg_hrv": avg_hrv,
            "avg_respiration_rate": respiration,
            "movement_score": movement,
            "stages": {
                "awake": awake,
                "light": light,
                "deep": deep,
                "rem": rem
            }
        }
        sleep_history.append(sleep_entry)
    return sleep_history[::-1]

def scale_sleep_history_to_90_seconds(sleep_history, target_duration_sec=90):
    scaled_history = []
    for day in sleep_history:
        total_min = day["duration_minutes"]
        scale_factor = target_duration_sec / total_min

        scaled_stages = {k: round(v * scale_factor, 1) for k, v in day["stages"].items()}

        scaled_day = {
            "date": day["date"],
            "duration_seconds": round(total_min * scale_factor, 1),
            "avg_heart_rate": day["avg_heart_rate"],
            "avg_hrv": day["avg_hrv"],
            "avg_respiration_rate": day["avg_respiration_rate"],
            "movement_score": day["movement_score"],
            "stages_seconds": scaled_stages
        }
        scaled_history.append(scaled_day)
    return scaled_history

# Generate original realistic data
# orig_sleep_history = generate_realistic_sleep_history(days=5)
# # Scale it to 90 seconds "night"
# scaled_sleep_history = scale_sleep_history_to_90_seconds(orig_sleep_history)

# Preview scaled data
import pprint
# pprint.pprint(scaled_sleep_history)


# generate fake oura data:

import random

def generate_oura_15sec_data(num_points=20):
    # Define approximate sleep stages sequence over 90 sec (can repeat cycles)
    sleep_stages = [
        "awake", "awake", "light", "light", "light", "deep", "deep", "deep",
        "rem", "rem", "light", "light", "deep", "deep", "rem", "rem",
        "light", "light", "awake", "awake"
    ][:num_points]

    data_points = []
    for i in range(num_points):
        stage = sleep_stages[i]

        if stage == "awake":
            hr = random.randint(70, 80)
            hrv = random.randint(20, 35)
            movement = round(random.uniform(0.4, 0.6), 2)
            respiration = round(random.uniform(15.5, 17.0), 1)
        elif stage == "light":
            hr = random.randint(60, 68)
            hrv = random.randint(40, 55)
            movement = round(random.uniform(0.2, 0.4), 2)
            respiration = round(random.uniform(13.5, 16.0), 1)
        elif stage == "deep":
            hr = random.randint(52, 58)
            hrv = random.randint(60, 80)
            movement = round(random.uniform(0.1, 0.25), 2)
            respiration = round(random.uniform(11.5, 13.5), 1)
        elif stage == "rem":
            hr = random.randint(58, 65)
            hrv = random.randint(45, 60)
            movement = round(random.uniform(0.05, 0.2), 2)
            respiration = round(random.uniform(12.5, 14.5), 1)

        data_points.append({
            "timestamp_sec": i * 15,
            "sleep_stage": stage,
            "heart_rate": hr,
            "hrv": hrv,
            "respiration_rate": respiration,
            "movement_score": movement
        })
    return data_points

# Generate and preview
simulated_oura_15s = generate_oura_15sec_data()
import pprint
pprint.pprint(simulated_oura_15s)
