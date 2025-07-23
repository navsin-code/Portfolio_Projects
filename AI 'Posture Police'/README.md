# 🧘‍♂️ AI Posture Police

**AI Posture Police** is a web-based application designed to help students and remote workers improve their posture during prolonged sitting.  
This app provides **real-time posture feedback**, **gamified motivation** (e.g. streaks, animations), and **productivity tools** like meeting reminders and a to-do list.  
It uses simulated or real data sent from a local machine to track posture, addressing user needs identified through a survey.

---

## ✨ Features

- **Real-Time Posture Feedback:**  
  Tracks posture as *Upright* or *Slouch* using simulated or real Arduino data.

- **Gamification:**  
  Earn streaks for good posture with animations (e.g. a fox after 30 minutes) and celebrations (e.g. confetti for goals).

- **Meeting Reminders:**  
  Schedule meetings and get browser-based alerts to correct posture during online classes.

- **Progress Tracking:**  
  Visualize posture data on a live graph and track streaks on a leaderboard.

- **To-Do List:**  
  Manage tasks to boost productivity alongside posture monitoring.

- **Privacy-Focused:**  
  Non-invasive design (no cameras) with offline functionality for core features.

---

## 📋 Prerequisites

To run this project, you'll need:

- **Python 3.10+** for running the Flask app locally.  
- **Arduino (Optional):** For real posture data, an Arduino with a posture sensor connected via serial port (e.g. `COM9`).

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-posture-police.git
cd ai-posture-police
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### `requirements.txt` includes:

```
flask
gunicorn
```

### 3. (Optional) Set Up Arduino for Real Data

- Connect your Arduino to your laptop (e.g. `COM9`).
- Install additional dependencies:

```bash
pip install pyserial requests
```

- Use the `send_arduino_data.py` script to send real data to the cloud app (see [Usage](#-usage)).

---

## 🚀 Usage

### Run Locally

**Start the Flask App:**

```bash
python main.py
```

App will run at:  
📍 [http://localhost:8000](http://localhost:8000)

**Access the App in Browser:**

1. Enter your name, age, purpose, and posture goal (in hours).
2. Navigate through the app:
   - Track posture
   - Schedule meetings
   - Manage tasks

### (Optional) Send Real Arduino Data

```bash
python send_arduino_data.py
```

- Ensure Arduino is connected
- Edit the `app_url` in `send_arduino_data.py` to point to your deployed app:  
  Example:

```python
app_url = "https://posturepolice.codes/update_posture"
```

---

## 📂 Project Structure

```
ai-posture-police/
├── main.py               # Flask app
├── send_arduino_data.py  # Script to send Arduino data
├── requirements.txt      # Python dependencies
├── Procfile              # DigitalOcean deployment config
├── runtime.txt           # Python version info
├── templates/            # HTML pages
│   ├── welcome.html
│   ├── index.html
│   ├── progress.html
│   ├── leaderboard.html
│   ├── meetings.html
│   └── todos.html
└── static/               # CSS, JS, images
```

---
