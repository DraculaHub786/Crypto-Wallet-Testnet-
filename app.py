from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import os, json
from pathlib import Path
from dotenv import load_dotenv

# === Load .env file ===
load_dotenv()

# === Configuration from .env ===
FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG_FLAG = os.getenv("FLASK_DEBUG", "0") == "1"
PORT = int(os.getenv("PORT", 5000))

LOG_SECRET = os.getenv("LOG_SECRET", None)
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "1") == "1"

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:8000,http://127.0.0.1:8000"
).split(",")

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
DATA_FILE = os.path.join(DATA_DIR, "tx_log.json")

# === Ensure data directory & file exist ===
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# === Flask App Setup ===
app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# === Helper Functions ===
def load_logs():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_logs(logs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

# === Routes ===
@app.route("/log", methods=["GET"])
def get_log():
    return jsonify(load_logs())

@app.route("/log", methods=["POST"])
def add_log():
    # Check authentication if required
    incoming_secret = request.headers.get("X-LOG-SECRET", "").strip()
    if REQUIRE_AUTH:
        if not LOG_SECRET:
            return jsonify({"status": "error", "reason": "Server not configured for logging"}), 403
        if incoming_secret != LOG_SECRET:
            return jsonify({"status": "error", "reason": "Invalid log secret"}), 403

    # Ensure JSON payload
    if not request.is_json:
        return jsonify({"status": "error", "reason": "Invalid content type"}), 415

    # Limit body size
    if request.content_length and request.content_length > 1024:
        return jsonify({"status": "error", "reason": "Payload too large"}), 413

    data = request.get_json(silent=True) or {}
    allowed_keys = ["time", "from", "to", "value", "hash", "network", "note"]
    safe_entry = {k: str(data.get(k))[:200] for k in allowed_keys if k in data and data.get(k) is not None}

    logs = load_logs()
    logs.insert(0, safe_entry)
    save_logs(logs)

    return jsonify({"status": "ok", "stored": safe_entry})

# === Serve Frontend ===
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_frontend(path):
    frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
    safe_path = os.path.normpath(os.path.join(frontend_dir, path))
    if not safe_path.startswith(os.path.abspath(frontend_dir)):
        abort(404)
    if not path:
        path = "index.html"
    return send_from_directory(frontend_dir, path)

# === Run App ===
if __name__ == "__main__":
    if DEBUG_FLAG:
        print("[WARNING] Debug mode is enabled. Do NOT use in production.")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG_FLAG)
