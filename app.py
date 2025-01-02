from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# File to store chat logs
CHAT_LOG_FILE = "chat_logs.json"

def load_chat_logs():
    """Load existing chat logs from the file."""
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r") as file:
            return json.load(file)
    return []

def save_chat_logs(logs):
    """Save chat logs to the file."""
    with open(CHAT_LOG_FILE, "w") as file:
        json.dump(logs, file, indent=2)

@app.route("/log-chat", methods=["POST"])
def log_chat():
    """Endpoint to receive and log chat data."""
    data = request.json
    if not data or "user_input" not in data or "gpt_response" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Create a log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": data["user_input"],
        "gpt_response": data["gpt_response"]
    }

    # Load existing logs and append the new entry
    chat_logs = load_chat_logs()
    chat_logs.append(log_entry)
    save_chat_logs(chat_logs)

    return jsonify({"status": "success"}), 200

@app.route("/get-logs", methods=["GET"])
def get_logs():
    """Endpoint to retrieve chat logs."""
    chat_logs = load_chat_logs()
    return jsonify(chat_logs), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))