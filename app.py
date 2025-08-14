from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, json

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

DATA_FILE = "tx_log.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/log", methods=["GET"])
def get_log():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/log", methods=["POST"])
def add_log():
    data = request.json or {}
    with open(DATA_FILE, "r") as f:
        arr = json.load(f)
    arr.insert(0, data)
    with open(DATA_FILE, "w") as f:
        json.dump(arr, f, indent=2)
    return jsonify({"status":"ok"})

# Serve frontend static files
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_frontend(path):
    frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
    if path == "" or path is None:
        path = "index.html"
    return send_from_directory(frontend_dir, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
