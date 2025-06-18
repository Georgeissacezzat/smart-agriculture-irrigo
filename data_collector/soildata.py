import requests
from src.models import SoilReport, Land 
from src.database import SessionLocal 
import logging


logging.basicConfig(level=logging.INFO)


SOIL_API_TEMPLATE = "http://api.agromonitoring.com/agro/1.0/soil?lat={lat}&lon={lon}&appid=9b757a467958fb4429322f76414baf6c"


def fetch_and_store_soil_data():
    db = SessionLocal() 
    try:
        lands = db.query(Land).all()

        for land in lands:
            lat, lon = land.lat, land.lon
            soil_url = SOIL_API_TEMPLATE.format(lat=lat, lon=lon)
            response = requests.get(soil_url)

            if response.status_code == 200:
                soil_data = response.json()
                new_soil_entry = SoilReport(
                    land_id=land.land_id,
                    t10=soil_data.get("t10"),
                    moisture=soil_data.get("moisture"),
                    t0=soil_data.get("t0"),
                )
                db.add(new_soil_entry)
                logging.info(f"Soil data saved for land {land.land_id}")

            else:
                logging.warning(f"Failed to fetch soil data for land {land.land_id}, status: {response.status_code}")

        db.commit()

    except Exception as e:
        logging.error(f"Error in fetch_and_store_soil_data: {e}")

    finally:
        db.close()