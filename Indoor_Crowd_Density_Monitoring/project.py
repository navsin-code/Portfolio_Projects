import time
import pandas as pd
import joblib
from Adafruit_IO import Client
from twilio.rest import Client as TwilioClient

# Adafruit IO credentials
ADAFRUIT_IO_USERNAME = "USERNAME"
ADAFRUIT_IO_KEY = "IO KEY"

# Twilio credentials
TWILIO_ACCOUNT_SID = "SID"
TWILIO_AUTH_TOKEN = "AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "NUMBER1"
TO_PHONE_NUMBER = "NUMBER2"

# Initialize Adafruit IO client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Initialize Twilio client
twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Load the trained model
model = joblib.load('crowd_density_linear_model.pkl')

# Normalization ranges
C_min, C_max = 400, 5000  # eCO2 (ppm)
V_min, V_max = 0, 1000    # TVOC (ppb)
E_min, E_max = 0, 1000    # EtOH (ppb)
I_min, I_max = 0, 500     # IAQ (unitless)

# Function to classify crowd density
def classify_density(density):
    if density < 0.3:
        return "Low"
    elif 0.3 <= density < 0.7:
        return "Medium"
    elif 0.7 <= density < 1.0:
        return "High"
    else:
        return "Critical"

# Function to get suggestions
def get_suggestion(density_class):
    if density_class == "Low":
        return "Normal conditions, no action needed."
    elif density_class == "Medium":
        return "Monitor occupancy, ensure ventilation."
    elif density_class == "High":
        return "Increase ventilation, consider crowd management."
    else:
        return "Immediate action: reduce occupancy, enhance airflow."

# Main loop to fetch live data and predict crowd density
while True:
    try:
        # Dictionary to store sensor readings
        sensor_data = {
            'eCO2': None,
            'tvoc': None,
            'EtOH': None,
            'indoor-aqi': None
        }

        # Fetch all feeds
        feeds = aio.feeds()
        for feed in feeds:
            if feed.name != "LED":  # Skip non-sensor feeds
                data = aio.receive(feed.key)
                print(f"{feed.name}: {data.value}")
                if feed.name.lower() == 'eco2':
                    sensor_data['eCO2'] = float(data.value)
                elif feed.name.lower() == 'tvoc':
                    sensor_data['tvoc'] = float(data.value)
                elif feed.name.lower() == 'etoh':
                    sensor_data['EtOH'] = float(data.value)
                elif feed.name.lower() == 'indoor-aqi':
                    sensor_data['indoor-aqi'] = float(data.value)

        # Check if all required sensor data is available
        if all(value is not None for value in sensor_data.values()):
            # Create a DataFrame with the live data
            new_data = pd.DataFrame([sensor_data])

            # Normalize the data
            new_data['C_norm'] = (new_data['eCO2'] - C_min) / (C_max - C_min)
            new_data['V_norm'] = (new_data['tvoc'] - V_min) / (V_max - V_min)
            new_data['E_norm'] = (new_data['EtOH'] - E_min) / (E_max - E_min)
            new_data['I_norm'] = (new_data['indoor-aqi'] - I_min) / (I_max - I_min)

            # Select features for prediction
            X_new = new_data[['C_norm', 'V_norm', 'E_norm', 'I_norm']]

            # Predict crowd density
            prediction = model.predict(X_new)[0]

            # Classify and get suggestion
            density_class = classify_density(prediction)
            suggestion = get_suggestion(density_class)

            print(f"Class: {density_class}")
            print(f"Suggestion: {suggestion}\n")

            # Send SMS if crowd density is High
            if density_class == "High":
                message = twilio_client.messages.create(
                    body="Alert: Crowd density is High! Suggestion: Increase ventilation, consider crowd management.",
                    from_=TWILIO_PHONE_NUMBER,
                    to=TO_PHONE_NUMBER
                )
                print(f"SMS sent successfully! Message SID: {message.sid}")

        else:
            print("Incomplete sensor data received. Waiting for next cycle...")

    except Exception as e:
        print(f"Error: {e}")

    # Wait 30 seconds before the next reading
    time.sleep(30)