import json
import os
from flask import Flask, jsonify

# Create the Flask application object.
app = Flask(__name__)

# Use the directory of this script so the JSON file is loaded correctly.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "fake_tickets.json")

@app.get("/tickets")
def get_tickets():
    """Return all tickets from fake_tickets.json as JSON."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data)

@app.get("/health")
def health():
    """Health check endpoint to verify API is running."""
    return jsonify({"status": "API Running"}), 200

if __name__ == "__main__":
    print("Starting Flask mock API on http://127.0.0.1:5000")
    print("Endpoint: GET /tickets")
    app.run(debug=False)
