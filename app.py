from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import os
from waitress import serve

# ================= FLASK =================
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

# ================= DATABASE =================
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://balisudhir1552005_db_user:12345@cluster0.gy0d1dh.mongodb.net/?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI)
db = client["smart_agro"]

sensor_collection = db["agro_sensor_data"]

print("✅ MongoDB Connected")

# ================= TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))


# ================= FRONTEND =================
@app.route('/')
def index():
    return send_from_directory('../frontend', 'viewdata.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('../frontend', path)


# ================= SAVE SENSOR DATA =================
@app.route('/sensors/data', methods=['POST'])
def save_sensor_data():
    try:
        data = request.get_json(force=True)

        ph = float(data.get("ph"))
        turbidity = float(data.get("turbidity"))
        soil = float(data.get("soil_moisture"))

        now = datetime.now(timezone.utc)

        sensor_collection.insert_one({
            "ph": ph,
            "turbidity": turbidity,
            "soil_moisture": soil,
            "timestamp": now
        })

        return jsonify({"message": "Data saved"}), 200

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Internal error"}), 500


# ================= GET LATEST DATA =================
@app.route('/sensors/latest', methods=['GET'])
def latest_data():
    d = sensor_collection.find_one(sort=[("timestamp", -1)])

    if not d:
        return jsonify({"message": "No data"}), 404

    return jsonify({
        "ph": d["ph"],
        "turbidity": d["turbidity"],
        "soil_moisture": d["soil_moisture"],
        "timestamp": d["timestamp"]
        .astimezone(IST)
        .strftime("%Y-%m-%d %H:%M:%S")
    })


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Server running on {port}")
    serve(app, host="0.0.0.0", port=port)