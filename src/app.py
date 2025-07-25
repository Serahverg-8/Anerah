import json
import os
from flask import Flask, request, jsonify, render_template
from agent import predict_sleep_stage

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")

# Ensure feedback file exists
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_stage", methods=["POST"])
def predict_stage():
    data = request.get_json(force=True)
    hour = data.get("hour")
    mood = data.get("mood", None)

    if hour is None:
        return jsonify({"error": "Missing required parameter: hour"}), 400

    try:
        result = predict_sleep_stage(hour, mood)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback = request.get_json(force=True)
    if not feedback:
        return jsonify({"error": "No feedback provided"}), 400

    # Load existing feedback
    with open(FEEDBACK_FILE, "r") as f:
        all_feedback = json.load(f)

    # Append new feedback with timestamp
    feedback["timestamp"] = int(os.times()[4])  # simple timestamp
    all_feedback.append(feedback)

    # Save back
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(all_feedback, f, indent=2)

    return jsonify({"message": "Feedback received, thank you!"})

if __name__ == "__main__":
    app.run(debug=True)
