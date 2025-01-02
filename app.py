from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Hardcoded API key (for demonstration purposes)
API_KEY = "your-secret-api-key"

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

@app.route("/")
def index():
    """Serve the main UI page."""
    return render_template("index.html")

@app.route("/log-chat", methods=["POST"])
def log_chat():
    """Endpoint to receive and log chat data."""
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data or "user_input" not in data or "gpt_response" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Log the chat
    chat_logs = load_chat_logs()
    chat_logs.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": data["user_input"],
        "gpt_response": data["gpt_response"]
    })
    save_chat_logs(chat_logs)

    return jsonify({"status": "success"}), 200

@app.route("/get-logs", methods=["GET"])
def get_logs():
    """Endpoint to retrieve chat logs."""
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    # Retrieve logs
    chat_logs = load_chat_logs()
    return jsonify(chat_logs), 200

def authenticate(request):
    """Check if the request contains a valid API key."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header == f"Bearer {API_KEY}":
        return True
    return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))