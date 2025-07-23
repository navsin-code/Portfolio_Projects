# linear_model.py
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from data_prep import prepare_data, split_data
import joblib  # Add this import

# Get the preprocessed data
X, y = prepare_data()

# Split the data
X_train, X_test, y_train, y_test = split_data(X, y)

# Train a simple linear regression model to estimate weights
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Predict crowd density
y_pred_linear = linear_model.predict(X_test)

# Evaluate
mse_linear = mean_squared_error(y_test, y_pred_linear)
r2 = r2_score(y_test, y_pred_linear)
print(f"Linear Model MSE: {mse_linear}")
print(f"R-squared: {r2}")

# Weights
weights = linear_model.coef_
print(f"Weights: w1={weights[0]}, w2={weights[1]}, w3={weights[2]}, w4={weights[3]}")

# Save the trained model
joblib.dump(linear_model, 'crowd_density_linear_model.pkl')
print("Model saved as 'crowd_density_linear_model.pkl'")

# Function to classify predicted crowd density
def classify_density(density):
    if density < 0.3:
        return "Low"
    elif 0.3 <= density < 0.7:
        return "Medium"
    elif 0.7 <= density < 1.0:
        return "High"
    else:
        return "Critical"

# Classify predictions
y_pred_classes = [classify_density(pred) for pred in y_pred_linear]
for i in range(5):
    print(f"Predicted Density: {y_pred_linear[i]:.2f}, Class: {y_pred_classes[i]}")