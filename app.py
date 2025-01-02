from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def authenticate(request):
    """Check if the request contains a valid API key."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header == f"Bearer {API_KEY}": # type: ignore
        return True
    return False

@app.route("/log-chat", methods=["POST"])
def log_chat():
    """Endpoint to receive and log chat data."""
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data or "user_input" not in data or "gpt_response" not in data:
        return jsonify({"error": "Invalid data"}), 400

    # Log the chat (your existing logic)
    return jsonify({"status": "success"}), 200

@app.route("/get-logs", methods=["GET"])
def get_logs():
    """Endpoint to retrieve chat logs."""
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    # Retrieve logs (your existing logic)
    return jsonify([]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))