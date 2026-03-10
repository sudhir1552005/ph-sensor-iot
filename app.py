from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb+srv://balisudhir1552005_db_user:12345@cluster0.gy0d1dh.mongodb.net/?retryWrites=true&w=majority")
db = client["smart_agro"]
collection = db["ph_data"]

# Homepage
@app.route("/")
def home():
    data = list(collection.find().sort("time", -1).limit(20))
    return render_template("index.html", data=data)

# API to receive sensor data
@app.route("/sensor", methods=["POST"])
def sensor():

    sensor_data = request.json

    record = {
        "moisture": sensor_data["moisture"],
        "ph": sensor_data["ph"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collection.insert_one(record)

    return jsonify({"status":"data stored"})

# SAMPLE DATA ROUTE
@app.route("/sample")
def sample():

    sample_data = {
        "moisture": 55,
        "ph": 6.85,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collection.insert_one(sample_data)

    return "Sample data inserted!"

if __name__ == "__main__":
    app.run()