from flask import Flask, render_template, request, current_app
from flask_mqtt import Mqtt
import os
from datetime import datetime
import json

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'localhost' # Replace with your MQTT broker's IP if not local
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_TOPIC'] = 'access/result'

mqtt = Mqtt(app)
# In-memory data structure to simulate database
# This will be reset every time the app restarts.
attendance_data = []
student_schedule = {
    "CSAI1001": ["BSB214", "ECG-01", "ASG-13"],
    "SE2001": ["BSB214", "ASG-13"],
    "ITM3006": ["ECG-01", "ASG-13"]
}# List of all students and their enrolled classes (locations)

@app.route("/")
def index():
    student_summary = {}
    for student_id in student_schedule:
        classes = student_schedule[student_id]

        # Weight mapping for attendance decisions
        decision_weights = {
            "granted": 1.0,
            "late": 0.5  # You can change this to any partial value you want
        }

        # Track the highest credit per location per student
        location_credits = {}
        for entry in attendance_data:
            if entry["student_id"] == student_id and entry["location"] in classes:
                key = (student_id, entry["location"])
                weight = decision_weights.get(entry["decision"], 0)
                location_credits[key] = max(location_credits.get(key, 0), weight)

        # Sum all credit scores and calculate attendance percentage
        earned_credits = sum(location_credits.values())
        attendance_rate = round((earned_credits / len(classes)) * 100, 1) if classes else 0

        student_summary[student_id] = {
            "total_classes": len(classes),
            "classes_attended": earned_credits,
            "attendance_rate": attendance_rate,
            "details": [entry for entry in attendance_data if entry["student_id"] == student_id]
        }

    return render_template("index.html", summary=student_summary, config=current_app.config)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """
    Callback function for when the MQTT client connects to the broker.
    Subscribes to the defined MQTT topic upon successful connection.
    """
    if rc == 0:
        print("Connected to MQTT Broker!")
        mqtt.subscribe(app.config['MQTT_TOPIC'])
    else:
        print(f"Failed to connect to MQTT Broker with code: {rc}")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    """
    Callback function for when a message is received on the subscribed topic.
    Parses the JSON payload and appends it to the in-memory attendance_data.
    """
    try:
        payload = json.loads(message.payload.decode())

        # Validate essential fields in the payload
        required_fields = ["student_id", "location", "timestamp", "decision"]
        if not all(field in payload for field in required_fields):
            print(f" Received incomplete message: {payload}. Missing required fields.")
            return
        # Store attendance record
        attendance_data.append({
            "student_id": payload["student_id"],
            "location": payload["location"],
            "timestamp": payload["timestamp"],
            "decision": payload["decision"],
            "reason": payload.get("reason", "")
        })
        print(f"🟢 Attendance received: {payload['student_id']} - {payload['decision']} at {payload['location']}")

    except json.JSONDecodeError:
        print(f" Error decoding JSON from message: {message.payload.decode()}")
    except Exception as e:
        print(f" An unexpected error occurred while processing message: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
