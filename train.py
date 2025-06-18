import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATASET_PATH = "src/data/Final_Data.csv"
MODEL_PATH = "src/ml/rf_model.pkl"

crop_mapping = {
    "Wheat": 1,
    "Corn": 2,
    "Cotton": 3,
    "Potatoes": 4,
    "Olives": 5,
    "Tomatoes": 6,
    "Grapes": 7
}

soil_type_mapping = {
    "clay": 1,
    "sandy": 2,
    "loamy": 3
}

df = pd.read_csv(DATASET_PATH)


df["crop_type"] = df["crop_type"].map(crop_mapping)
df["soil_type"] = df["soil_type"].map(soil_type_mapping)


# Define target and features
target = 'water_irrigation_amount_log'
features = ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m',
            'crop_days', 'crop_type', 'soil_moisture', 'soil_type']

X = df[features]
y = df[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Save model
joblib.dump(model, MODEL_PATH)

# Output results
print(f"✅ Model trained and saved to {MODEL_PATH}")
print(f"📊 MAE: {mae:.4f}, MSE: {mse:.4f}, R2 Score: {r2:.4f}")