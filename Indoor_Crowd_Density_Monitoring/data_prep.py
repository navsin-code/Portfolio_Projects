# data_preparation.py
import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data():
    # Load the dataset
    data = pd.read_csv(r"MODEL_PATH")

    # Define normalization ranges from the document
    C_min, C_max = 400, 5000  # eCO2 (ppm)
    V_min, V_max = 0, 1000    # TVOC (ppb)
    E_min, E_max = 0, 1000    # EtOH (ppb)
    I_min, I_max = 0, 500     # IAQ (unitless)

    # Normalize the features
    data['C_norm'] = (data['eCO2'] - C_min) / (C_max - C_min)
    data['V_norm'] = (data['tvoc'] - V_min) / (V_max - V_min)
    data['E_norm'] = (data['EtOH'] - E_min) / (E_max - E_min)
    data['I_norm'] = (data['indoor-aqi'] - I_min) / (I_max - I_min)

    # Map categorical crowd_density to numeric values
    density_mapping = {
        'low': 0.15,
        'medium': 0.5,
        'high': 0.85,
        'critical': 1.5
    }
    data['crowd_density_numeric'] = data['crowd_density'].map(density_mapping)

    # Features and target
    X = data[['C_norm', 'V_norm', 'E_norm', 'I_norm']]
    y = data['crowd_density_numeric']  # Use numeric target

    return X, y

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    X, y = prepare_data()
    X_train, X_test, y_train, y_test = split_data(X, y)