from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time
import random
from datetime import datetime, timedelta
import serial
import logging

app = Flask(__name__)

# Global user data 
user_data = {
    "name": "",
    "age": 0,
    "purpose": "",
    "goal_hours": 0,
    "current_streak": 0,  # in seconds
    "best_streak": 0,  # Track best streak for leaderboard
    "posture_data": [],  # (timestamp, status)
    "meetings": [],
    "todos": []
}

goal_seconds = 0
running = True
arduino_serial = None
last_posture_status = "Upright"

# Setup logging
logging.basicConfig(level=logging.DEBUG)


def initialize_arduino():
    global arduino_serial
    try:
        arduino_serial = serial.Serial('COM6', 9600, timeout=1)
        time.sleep(2)  # Allow Arduino to initialize
        logging.info("Arduino connected successfully on COM6")
        print(" Arduino connected successfully on COM6")
        return True
    except Exception as e:
        logging.error(f"Failed to connect to Arduino on COM6: {e}")
        print(f" Failed to connect to Arduino on COM6: {e}")
        return False


def start_posture_monitoring():
    global last_posture_status, arduino_serial

    # Try to initialize Arduino connection
    if not initialize_arduino():
        logging.warning("Arduino not connected, using fallback monitoring")
        print(" Arduino not connected, using fallback monitoring")

    while running:
        posture = last_posture_status  # Start with last known status

        # Try to read from Arduino
        if arduino_serial and arduino_serial.is_open:
            try:
                # Check for data more frequently
                while arduino_serial.in_waiting > 0:  # Process all available data
                    line = arduino_serial.readline().decode('utf-8', errors='ignore').strip()
                    
                    if not line:  # Skip empty lines
                        continue
                    
                    # DEBUG: Print exactly what we receive
                    print(f" RAW Arduino data: '{line}'")
                    logging.debug(f"Arduino data: {line}")

                    # Check if it's a sensor reading (numeric) or status message
                    if line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                        # This is a raw sensor reading, skip it
                        print(f" Sensor reading: {line}")
                        continue
                        
                    # Check for posture status messages
                    line_lower = line.lower()
                    if "slouching detected" in line_lower:
                        posture = "Slouch"
                        print(" SLOUCHING DETECTED!")
                        logging.info("Slouching detected by Arduino sensor")
                        break  # Exit the while loop to process immediately
                            
                    elif "posture okay" in line_lower or "good posture" in line_lower:
                        posture = "Upright"
                        print(" GOOD POSTURE!")
                        break  # Exit the while loop to process immediately
                        
                    elif "debug:" in line_lower:
                        # Handle debug messages from Arduino
                        print(f" Arduino Debug: {line}")
                        continue
                        
                    elif "arduino ready" in line_lower:
                        print(" Arduino initialization complete!")
                        continue
                        
                    else:
                        # Unknown message, maintain last status
                        print(f" Unknown message: '{line}'")
                        
            except Exception as e:
                print(f" Error reading from Arduino: {e}")
                logging.error(f"Error reading from Arduino: {e}")
                # Try to reconnect
                try:
                    arduino_serial.close()
                except:
                    pass
                initialize_arduino()
        else:
            # Fallback when Arduino not connected - use random data for testing
            if random.random() < 0.05:  # 5% chance of slouching (reduced for testing)
                posture = "Slouch"
                print(" Simulated slouching (Arduino not connected)")
            else:
                posture = "Upright"

        # Only update data if posture actually changed
        if posture != last_posture_status:
            timestamp = datetime.now().isoformat()
            user_data["posture_data"].append({"time": timestamp, "status": posture})

            # Keep only recent entries in memory (last 100)
            if len(user_data["posture_data"]) > 100:
                user_data["posture_data"] = user_data["posture_data"][-100:]

            # Update streak logic
            if posture == "Upright":
                user_data["current_streak"] += 1
                # Update best streak if current streak is better
                if user_data["current_streak"] > user_data["best_streak"]:
                    user_data["best_streak"] = user_data["current_streak"]
                    print(f" New best streak: {user_data['best_streak']} seconds!")
                
                # Check for goal achievement
                goal_seconds_achieved = user_data["current_streak"]
                goal_hours_achieved = goal_seconds_achieved / 3600
                
                if (goal_seconds_achieved >= goal_seconds and 
                    goal_seconds > 0 and
                    goal_hours_achieved >= 0.1):  # At least 6 minutes before celebrating
                    
                    print(f" GOAL ACHIEVED! You sat straight for {goal_hours_achieved:.1f} hours!")
            else:
                user_data["current_streak"] = 0

            last_posture_status = posture
        
        # Much shorter sleep for faster response
        time.sleep(0.1)  # Check every 100ms instead of 1 second


def check_meeting_reminders():
    while running:
        now = datetime.now()
        updated_meetings = []
        for meeting in user_data["meetings"]:
            meeting_dt = datetime.fromisoformat(meeting["dateTime"])
            time_diff = (meeting_dt - now).total_seconds() / 60
            if time_diff > 0 and time_diff <= meeting["reminder"]:
                # Meeting reminder (console notification only)
                message_body = f"Meeting reminder: Your meeting is coming up on {meeting_dt.strftime('%B %d at %I:%M %p')}"
                print(f" {message_body}")
                logging.info(message_body)
            else:
                updated_meetings.append(meeting)
        
        user_data["meetings"] = updated_meetings
        time.sleep(60)  # Check every minute


@app.route('/')
def index():
    if not user_data["name"]:
        return render_template('welcome.html')
    return render_template('index.html', user=user_data)


@app.route('/submit_user', methods=['POST'])
def submit_user():
    user_data["name"] = request.form.get('name', 'User')
    user_data["age"] = int(request.form.get('age', 0))
    user_data["purpose"] = request.form.get('purpose', 'Meeting')
    user_data["goal_hours"] = float(request.form.get('goal_hours', 2))
    global goal_seconds
    goal_seconds = user_data["goal_hours"] * 3600

    # Start posture monitoring and meeting reminders
    threading.Thread(target=start_posture_monitoring, daemon=True).start()
    threading.Thread(target=check_meeting_reminders, daemon=True).start()
    return redirect(url_for('index'))


@app.route('/progress')
def progress():
    return render_template('progress.html', user=user_data)


@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = [
        {"name": "Varun", "streak": 25},
        {"name": "Priya", "streak": 20},
        {"name": "Likith", "streak": 18},
        {"name": user_data["name"], "streak": user_data["best_streak"] // 60},
        {"name": "Chithra", "streak": 12}
    ]
    leaderboard_data.sort(key=lambda x: x["streak"], reverse=True)
    return render_template('leaderboard.html', leaderboard=leaderboard_data, user=user_data)


@app.route('/meetings', methods=['GET', 'POST'])
def meetings():
    if request.method == 'POST':
        meeting_date = request.form.get('date')
        meeting_time = request.form.get('time')
        reminder_value = request.form.get('reminder', 5)
        reminder = int(reminder_value) if reminder_value else 5
        try:
            meeting_dt = datetime.strptime(f"{meeting_date} {meeting_time}", "%Y-%m-%d %H:%M")
            user_data["meetings"].append({"dateTime": meeting_dt.isoformat(), "reminder": int(reminder)})
        except ValueError:
            pass
    return render_template('meetings.html', user=user_data)


@app.route('/get_posture_data')
def get_posture_data():
    return jsonify({
        "posture_data": user_data["posture_data"][-50:],
        "current_streak": user_data["current_streak"],
        "goal_seconds": goal_seconds
    })


@app.route('/get_meetings')
def get_meetings():
    return jsonify(user_data["meetings"])


@app.route('/todos')
def todos():
    return render_template('todos.html', user=user_data)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    task = request.form.get('task', '').strip()
    if task:
        todo_item = {
            "id": len(user_data["todos"]) + 1,
            "task": task,
            "status": "to-do",  # to-do, in-progress, done
            "created_at": datetime.now().isoformat()
        }
        user_data["todos"].append(todo_item)
    return redirect(url_for('todos'))


@app.route('/update_todo_status', methods=['POST'])
def update_todo_status():
    todo_id_str = request.form.get('todo_id')
    new_status = request.form.get('status')

    if todo_id_str and new_status:
        todo_id = int(todo_id_str)
        for todo in user_data["todos"]:
            if todo["id"] == todo_id:
                todo["status"] = new_status
                break

    return jsonify({"success": True})


@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    todo_id_str = request.form.get('todo_id')

    if todo_id_str:
        todo_id = int(todo_id_str)
        user_data["todos"] = [todo for todo in user_data["todos"] if todo["id"] != todo_id]

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)