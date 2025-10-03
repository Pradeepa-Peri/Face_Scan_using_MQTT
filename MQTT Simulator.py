import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

MQTT_BROKER = "localhost" # Ensure this matches the Flask app's configuration
MQTT_PORT = 1883
MQTT_TOPIC = "access/result"

TEST_STUDENTS = ["CSAI1001", "SE2001", "ITM3006"]
STUDENT_CLASSES = {
    "CSAI1001": ["BSB214", "ECG-01", "ASG-13"],
    "SE2001": ["BSB214", "ASG-13"],
    "ITM3006": ["ECG-01", "ASG-13"]
}
TEST_TEACHERS = ["Dr. Smith", "Dr. Johnson", "Dr. Brown"]

def create_test_message():
    """Generates a random attendance record message."""
    student_id = random.choice(TEST_STUDENTS)
    location = random.choice(STUDENT_CLASSES[student_id])
    
    # Randomly decide if the decision is 'granted', 'denied', or 'late'
    decision = random.choices(["granted", "denied", "late"], weights=[0.7, 0.2, 0.1])[0]

    # Generate a reason based on the decision
    reason = ""
    if decision == "granted":
        reason = "Face recognized successfully"
    elif decision == "denied":
        reason = random.choice(["Face not in database", "Access denied for this location"])
    else: # late
        reason = "Late entry"

    return {
        "student_id": student_id,
        "face_id": student_id, # Assuming face_id is the same as student_id for simplicity
        "timestamp": datetime.now().strftime("%I:%M %p"),       
        "decision": decision,
        "reason": reason,
        "location": location,
        "module_teacher": random.choice(TEST_TEACHERS),
    }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker.")
    else:
        print("MQTT connection failed. Code:", rc)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except ConnectionRefusedError:
        print(f"Connection refused. Is the MQTT broker running at {MQTT_BROKER}:{MQTT_PORT}?")
        return

    client.loop_start() # Start a non-blocking loop for network traffic
    time.sleep(1) # Give a moment for the connection to establish
    count = 0
    try:
        while True:
            message = create_test_message()
            client.publish(MQTT_TOPIC, json.dumps(message))
            count += 1
            print(f"[{count}] Published for {message['student_id']} - {message['decision']} at {message['location']}")
            time.sleep(random.uniform(3, 8)) # Send messages at random intervals
    except KeyboardInterrupt:
        print(f"\n Stopped after sending {count} messages.")
    finally:
        client.loop_stop() # Stop the MQTT loop
        client.disconnect() # Disconnect from the broker
if __name__ == "__main__":
    main()
