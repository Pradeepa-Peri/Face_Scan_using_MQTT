#  Face Recognition Attendance System via MQTT

This project is a real-time **Student Attendance Monitoring Dashboard** that uses **face recognition data** published through the **MQTT protocol**. It simulates an end-to-end pipeline from identity validation (via face scan) to attendance recording and visualization using a Flask web app (which is my part being a group project).

---

## 📌 Key Features

-  Real-time attendance via MQTT messages
-  Simulated face scan decisions: `granted`, `denied`, or `late`
-  Location-based attendance tracking per student
-  Flask dashboard with class-wise summaries and decision insights
-  Continuous monitoring loop
-  Flowchart designed with **Canva** to visualize MQTT logic

---

## 🧰 Technologies Used

- **Python 3**
- **Flask** (Web dashboard)
- **paho-mqtt** (MQTT client for message handling)
- **Flask-MQTT** (MQTT integration with Flask)
- **Tailwind CSS** (Frontend styling)
- **Jinja2** (Template rendering)
- **Canva** (Flowchart design)

---

## 📂 Project Structure

![image](https://github.coventry.ac.uk/4005CMD2526MAYSEP/Face-Scan-using-MQTT/assets/7867/446f6b0b-8b07-4187-aaa6-c41077355a9e)


---

## ⚙️ How It Works

###  1. Simulated Face Scanning
The `mqtt_simulator.py` script mimics a camera system, publishing random face recognition decisions (e.g., `granted`, `denied`, `late`) along with a `timestamp`, `student_id` and `location`.

### 📡 2. MQTT Communication
Messages are sent over MQTT to the topic `access/result`. The Flask app (`app.py`) listens to this topic and updates an in-memory attendance record.

### 📊 3. Dashboard Visualization
Using Flask + Jinja2 + Tailwind CSS, a dashboard presents each student's:
-  Class locations
-  Attendance status
-  Attendance percentage (based on decisions)
-  Reason for decision

---

#### ▶️ How to Run the Project (Proper Bash Block):

```markdown
## ▶️ How to Run the Project

### ✅ Step 1: Install Requirements

Make sure Python 3 is installed, then run:

```bash
pip install flask flask-mqtt paho-mqtt

sudo apt-get update -y
sudo apt-get install mosquitto mosquitto-clients -y
mosquitto

### 2. Run Flask Dashboard

In one terminal, run the following command:

```bash
python3 app.py

In another terminal, run the following command:

```bash
python3 MQTT_Simulator.py

Thank you for checking out this project branch! 



