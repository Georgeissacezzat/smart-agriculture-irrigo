import joblib
import numpy as np
from sqlalchemy.orm import Session
from src.database import get_db, db
from src.models import SoilReport, WeatherReport, IrrigationDecision, Land



MODEL_PATH = "src/ml/rf_model.pkl"


model = joblib.load(MODEL_PATH)

def get_latest_weather_and_soil(land_id: int):
    latest_weather = db.query(WeatherReport).filter(WeatherReport.land_id == land_id).order_by(WeatherReport.timestamp.desc()).first()
    latest_soil = db.query(SoilReport).filter(SoilReport.land_id == land_id).order_by(SoilReport.timestamp.desc()).first()

    if not latest_weather or not latest_soil:
        return None, None, None, None

    return (
        latest_weather.temperature_2m,
        latest_weather.relative_humidity_2m,
        latest_weather.wind_speed_10m,
        latest_soil.moisture,
    )

def predict_irrigation_for_all_lands():
    lands = db.query(Land).all()

    for land in lands:
        crop_type = land.crop_type
        crop_days = land.crop_days
        soil_type = land.soil_type

        temperature, humidity, wind_speed, moisture = get_latest_weather_and_soil(land.land_id)

        if temperature is None:
            print(f"⚠️ Skipping land {land.land_id}: No recent weather/soil data.")
            continue


        X_input = np.array([[temperature, humidity, wind_speed, crop_days, crop_type, moisture, soil_type]])


        water_amount = round(float(model.predict(X_input)[0]), 2)
  
    
        irrigation_decision = IrrigationDecision(
            land_id=land.land_id,
            water_amount=water_amount
        )
        db.add(irrigation_decision)

    db.commit()
    print("✅ Predictions added to the database.")
