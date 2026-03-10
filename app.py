from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://balisudhir1552005_db_user:12345@cluster0.gy0d1dh.mongodb.net/smart_agro?retryWrites=true&w=majority&appName=Cluster0")

db = client["smart_agro"]
collection = db["ph_data"]

# Home page
@app.route("/")
def home():
    data = list(collection.find().sort("time",-1).limit(20))
    return render_template("index.html", data=data)

# ESP32 data receiver
@app.route("/sensor", methods=["POST"])
def sensor():

    data = request.get_json()

    record = {
        "moisture": data["moisture"],
        "ph": data["ph"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collection.insert_one(record)

    return jsonify({"status":"success"})


if __name__ == "__main__":
    app.run(debug=True)