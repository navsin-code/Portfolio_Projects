# Non-Invasive Crowd Density Estimation via Air Quality Monitoring

This repository contains the implementation of a non-invasive crowd density estimation system using air quality monitoring. The system leverages the **Renesas QC-BEKITPOC7 kit** with an **RA6E2 MCU**, **ZMOD4410**, and **HS4001 sensors** to monitor air quality parameters (**eCO₂**, **TVOC**, **EtOH**, **IAQ**) and estimate crowd density using a **linear regression model**. Data is transmitted to **Adafruit IO** via **MQTT**, visualized on a web dashboard, and critical density levels trigger **Twilio SMS alerts**.

## Project Overview

Crowd disasters in India, such as the **Hathras stampede (2024, 121 deaths)**, **Tirupati temple incident (2023)**, and **New Delhi railway station stampede (2025)**, highlight the need for effective crowd management. Traditional camera-based systems raise privacy concerns, especially in sensitive locations like temples and transit hubs. This project proposes a **privacy-preserving solution** that uses air quality data to estimate crowd density in real-time, avoiding invasive surveillance.

### Key Features

- **Non-Invasive Monitoring**: Uses ZMOD4410 and HS4001 sensors to measure eCO₂, TVOC, EtOH, and IAQ without visual data.
- **Linear Regression Model**: Predicts crowd density with high accuracy (**MSE**: 0.005, **R-squared**: 0.942).
- **Real-Time Data Transmission**: Sends sensor data to Adafruit IO via MQTT for cloud-based processing.
- **Web Dashboard**: Visualizes real-time and historical data on Adafruit IO.
- **Automated Alerts**: Triggers Twilio SMS notifications for **High** or **Critical** density levels to prompt actions like entry restriction or ventilation increase.
- **Scalable and Privacy-Respecting**: Suitable for temples, transit hubs, and other sensitive indoor environments.

## System Architecture

The system integrates the following components:

- **Hardware**:
  - **Renesas QC-BEKITPOC7 Kit**: Powered by the RA6E2 MCU, interfaced via Quick Connect Studio.
  - **ZMOD4410 Sensor**: Measures eCO₂, TVOC, and EtOH using metal oxide (MOX) technology.
  - **HS4001 Sensor**: Measures indoor air quality (IAQ).
- **Data Collection**: Sensors read air quality data every 30 seconds.
- **Data Transmission**: Data is sent to Adafruit IO using the MQTT protocol.
- **Data Processing**: A linear regression model normalizes and analyzes data to predict crowd density.
- **Visualization**: Adafruit IO dashboard displays real-time data, historical trends, and control options.
- **Alert System**: Twilio SMS alerts are sent for high/critical density levels, suggesting actions like increasing ventilation or limiting entry.


## AI Model Details

The system uses a **linear regression model** to estimate crowd density from normalized air quality features:

- **Features**: eCO₂ (C_norm), TVOC (V_norm), EtOH (E_norm), IAQ (I_norm).
- **Target**: Crowd density (mapped to numeric values).
- **Normalization**: Features are normalized to ensure consistent scaling (Equation 1 in the paper).
- **Model Equation**: Linear regression model predicts density as a function of normalized features.

### Performance Metrics

- **Mean Squared Error (MSE)**: 0.005, indicating low prediction error.
- **R-squared**: 0.942, showing 94.2% similarity between predicted and actual density values, demonstrating strong correlation.

The coefficients suggest that **TVOC** has the most significant influence on crowd density predictions, followed by **IAQ**, **EtOH**, and **eCO₂**.

### Classification

Predicted density values are categorized into four levels:

- **Low**: <15
- **Medium**: 15–30
- **High**: 30–50
- **Critical**: >50

**High** or **Critical** levels trigger Twilio SMS alerts with actionable suggestions.

## Setup Instructions

### Hardware Setup

1. **Assemble the Renesas QC-BEKITPOC7 Kit**:
   - Connect the **ZMOD4410** and **HS4001** sensors to the **RA6E2 MCU** via the Quick Connect Studio platform.
   - Ensure proper wiring for power, ground, and I2C/SPI interfaces.
2. **Flash Firmware**:
   - Use a **J-Link debugger** to flash the firmware to the RA6E2 MCU.
   - Example command for nRF52 (adjust for RA6E2):
     ```bash
     nrfjprog --program firmware.hex --sectorerase
     nrfjprog --reset
     ```
   - Firmware should read sensor data and publish to Adafruit IO via MQTT.
3. **Configure Wi-Fi**:
   - Update the firmware with your Wi-Fi SSID and password.

### Software Setup

1. **Python Environment**:
   - Use **Python 3.12**
   - Install dependencies:
     ```bash
     pip install Adafruit_IO pandas scikit-learn joblib
     ```
2. **Adafruit IO**:
   - Create an account at [io.adafruit.com](https://io.adafruit.com) 
   - Create feeds: `etoh`, `eco2`, `indoor-aqi`, `tvoc`.
   - Obtain your **API key** from **My Key** and update in the code. **Note**: Regenerate the API key if you encounter "invalid API key" errors, as seen in previous tests.
3. **Twilio Setup**:
   - Create a Twilio account and configure SMS notifications for high/critical density alerts.
   - Update the Python script with your Twilio SID, auth token, and phone numbers.

### Firmware

The microcontroller firmware reads sensor data every 30 seconds and publishes to Adafruit IO feeds. Example (simplified Arduino code for RA6E2):

### Regression Plot
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/c1ce98ab-9f57-4e7a-85ce-2c35407468ad" />


### Residual Plot
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/d1a324da-1312-484a-a89b-06a2f70875aa" />
