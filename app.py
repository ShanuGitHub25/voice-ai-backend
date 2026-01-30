from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# This is YOUR API key (you decide it)
MY_API_KEY = "test123"

# Google AI Studio key (from .env)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/voice-detect", methods=["POST"])
def voice_detect():

    # 1. Check API key
    if request.headers.get("x-api-key") != MY_API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    # 2. Get input
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    user_text = data["text"]

    # 3. Send to Google AI
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GOOGLE_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": f"Tell if this voice text is AI or Human and respond in JSON with label and confidence:\n{user_text}"
            }]
        }]
    }

    response = requests.post(url, json=payload)
    result = response.json()

    return jsonify({
        "result": result
    })

if __name__ == "__main__":
    app.run()
