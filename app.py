from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
import json

app = Flask(__name__)

# Fetch the API key from an environment variable
API_KEY = os.getenv("API_KEY")

# File to store chat logs
CHAT_LOG_FILE = "chat_logs.json"

def load_chat_logs():
    """Load existing chat logs from the file."""
    try:
        if os.path.exists(CHAT_LOG_FILE):
            with open(CHAT_LOG_FILE, "r") as file:
                return json.load(file)
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in chat logs: {e}")
        return []
    except Exception as e:
        print(f"Error loading chat logs: {e}")
        return []

def save_chat_logs(logs):
    """Save chat logs to the file."""
    try:
        with open(CHAT_LOG_FILE, "w") as file:
            json.dump(logs, file, indent=2)
    except Exception as e:
        print(f"Error saving chat logs: {e}")

@app.route("/")
def index():
    """Serve the main UI page."""
    return render_template("index.html")

@app.route("/log-chat", methods=["POST"])
def log_chat():
    """Endpoint to receive and log chat data."""
    # Authenticate the request
    if not authenticate(request):
        return jsonify({"error": "Unauthorized: Invalid or missing API key"}), 401

    data = request.json
    if not data or "user_input" not in data or "response" not in data or "thought_process" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Log the chat
    chat_logs = load_chat_logs()
    chat_logs.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": data["user_input"],
        "response": data["response"],
        "thought_process": data["thought_process"]
    })
    save_chat_logs(chat_logs)

    return jsonify({"status": "success"}), 200

@app.route("/get-logs", methods=["GET"])
def get_logs():
    """Endpoint to retrieve chat logs."""
    try:
        print("Fetching logs...")
        chat_logs = load_chat_logs()
        print(f"Logs fetched: {chat_logs}")
        return jsonify(chat_logs), 200
    except Exception as e:
        print(f"Error in /get-logs: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

def authenticate(request):
    """Check if the request contains a valid API key."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header == f"Bearer {API_KEY}":
        return True
    return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))