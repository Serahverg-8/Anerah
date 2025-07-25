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
    # Serve your main UI page
    return render_template("index.html")

@app.route("/predict_stage", methods=["POST"])
def predict_stage():
    data = request.get_json(force=True)
    try:
        print("Received data:", data)  # log incoming
        result = predict_sleep_stage(data)
        print("Prediction result:", result)  # log outgoing
        return jsonify(result)
    except Exception as e:
        import traceback
        print("Error in /predict_stage:", traceback.format_exc())  # full error
        return jsonify({"error": str(e)}), 500

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback = request.get_json(force=True)
    if not feedback:
        return jsonify({"error": "No feedback provided"}), 400

    # Load existing feedback
    with open(FEEDBACK_FILE, "r") as f:
        all_feedback = json.load(f)

    # Append new feedback with timestamp (using time.time())
    import time
    feedback["timestamp"] = int(time.time())
    all_feedback.append(feedback)

    # Save back
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(all_feedback, f, indent=2)

    return jsonify({"message": "Feedback received, thank you!"})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
