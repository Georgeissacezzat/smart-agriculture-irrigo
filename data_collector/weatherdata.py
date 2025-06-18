import requests
from src.models import WeatherReport, Land
from src.database import SessionLocal 
import logging


logging.basicConfig(level=logging.INFO)


WEATHER_API_TEMPLATE = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"


def fetch_and_store_weather_data():
    db = SessionLocal() 
    try:
        lands = db.query(Land).all()

        for land in lands:
            lat, lon = land.lat, land.lon
            weather_url = WEATHER_API_TEMPLATE.format(lat=lat, lon=lon)
            response = requests.get(weather_url)

            if response.status_code == 200:
                weather_data = response.json().get("current", {})
                new_weather_entry = WeatherReport(
                    land_id=land.land_id,
                    temperature_2m=weather_data.get("temperature_2m"),
                    relative_humidity_2m=weather_data.get("relative_humidity_2m"),
                    apparent_temperature=weather_data.get("apparent_temperature"),
                    is_day=weather_data.get("is_day", 1),  
                    precipitation=weather_data.get("precipitation", 0.0),  
                    rain=weather_data.get("rain", 0.0),  
                    showers=weather_data.get("showers", 0.0),  
                    snowfall=weather_data.get("snowfall", 0.0),  
                    weather_code=weather_data.get("weather_code", 0),  
                    cloud_cover=weather_data.get("cloud_cover", 0),  
                    pressure_msl=weather_data.get("pressure_msl", 1013.25),  
                    surface_pressure=weather_data.get("surface_pressure", 1013.25),  
                    wind_speed_10m=weather_data.get("wind_speed_10m", 0.0),  
                    wind_direction_10m=weather_data.get("wind_direction_10m", 0),  
                    wind_gusts_10m=weather_data.get("wind_gusts_10m", 0.0)  
                )

                db.add(new_weather_entry)
                logging.info(f"Weather data saved for land {land.land_id}")

            else:
                logging.warning(f"Failed to fetch weather data for land {land.land_id}, status: {response.status_code}")

        db.commit()

    except Exception as e:
        logging.error(f"Error in fetch_and_store_weather_data: {e}")

    finally:
        db.close()


