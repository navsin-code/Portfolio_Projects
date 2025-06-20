**AI Posture Police**
AI Posture Police is a web-based application designed to help students and remote workers improve their posture during prolonged sitting.This app provides real-time posture feedback, gamified motivation (e.g.streaks, animations), and productivity tools like meeting reminders and a to-do list. It usesor real data sent from a local machine to track posture, addressing user needs identified through a survey.

✨**Features**
**Real-Time Posture Feedback:** Tracks posture as Upright or Slouch using simulated or real Arduino data.
**Gamification:** Earn streaks for good posture, with animations (e.g. a fox after 30 minutes) and celebrations (e.g. confetti for goals).
**Meeting Reminders:** Schedule meetings and get browser-based alerts to correct posture during online classes.
**Progress Tracking:** Visualize posture data on a live graph and track streaks on a leaderboard.
**To-Do List:** Manage tasks to boost productivity alongside posture monitoring.
**Privacy-Focused:** Non-invasive design (no cameras) with offline functionality for core features.

📋 **Prerequisites**
To run this project, you'll need:

**Python 3.10+:** For running the Flask app locally.
**Arduino (Optional):** For real posture data, an Arduino with a posture sensor connected via serial port (e.g. COM9).

🛠️ **Installation**

**Clone the Repository:**
'''git clone https://github.com/yourusername/ai-posture-police.git
cd ai-posture-police'''


**Install Dependencies:**
'''pip install -r requirements.txt'''

**The requirements.txt includes:**
flask
gunicorn


**(Optional) Set Up Arduino for Real Data:**

Connect your Arduino to your laptop (e.g. COM9).
Install additional dependencies on your local machine:pip install pyserial requests


Use the send_arduino_data.py script to send real data to the cloud app (see Usage below).



🚀** Usage**
Running Locally

**Start the Flask App:**
python main.py

The app will run at http://localhost:8000.

**Access the App:**

Open http://localhost:8000 in your browser.
On the welcome page, enter your name, age, purpose, and posture goal (in hours).
Navigate through the app to track posture, schedule meetings, and manage tasks.


**(Optional) Send Real Arduino Data:**

Run the send_arduino_data.py script on your laptop to send real posture data to the app (if deployed online):python send_arduino_data.py

Ensure your Arduino is connected and the app_url in the script points to your deployed app (e.g. https://posturepolice.codes/update_posture).


📂 **Project Structure**
ai-posture-police/
├── main.py              # Flask app
├── send_arduino_data.py # Script to send real Arduino data (run locally)
├── requirements.txt     # Python dependencies
├── Procfile             # DigitalOcean App Platform deployment config
├── runtime.txt          # Python version for DigitalOcean
├── templates/           # HTML templates
│   ├── welcome.html
│   ├── index.html
│   ├── progress.html
│   ├── leaderboard.html
│   ├── meetings.html
│   └── todos.html
└── static/              # CSS, JS, and other static files



