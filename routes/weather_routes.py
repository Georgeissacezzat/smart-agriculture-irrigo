from fastapi import status ,Depends , APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.models import WeatherReport 
from src.schemas import WeatherReportSchema
from src.database import get_db


router = APIRouter()


@router.get("/get-latest-weather-report/{id}")
async def get_latest_weather_report (id : int , db : Session = Depends(get_db)) -> dict :
    latest_report = (
        db.query(WeatherReport)
        .filter(WeatherReport.land_id == id)  
        .order_by(WeatherReport.timestamp.desc()) 
        .first()
    )
    if latest_report :
        return {
        "report_id": latest_report.report_id,
        "land_id": latest_report.land_id,
        "timestamp": latest_report.timestamp,
        "temperature_2m": latest_report.temperature_2m,
        "relative_humidity_2m": latest_report.relative_humidity_2m,
        "apparent_temperature": latest_report.apparent_temperature,
        "is_day": latest_report.is_day,
        "precipitation": latest_report.precipitation,
        "rain": latest_report.rain,
        "showers": latest_report.showers,
        "snowfall": latest_report.snowfall,
        "weather_code": latest_report.weather_code,
        "cloud_cover": latest_report.cloud_cover,
        "pressure_msl": latest_report.pressure_msl,
        "surface_pressure": latest_report.surface_pressure,
        "wind_speed_10m": latest_report.wind_speed_10m,
        "wind_direction_10m": latest_report.wind_direction_10m,
        "wind_gusts_10m": latest_report.wind_gusts_10m,
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Report found")


@router.get("/get-weather-reports/{id}" , response_model=List[WeatherReportSchema])
async def get_soil_reports(id: int, db: Session = Depends(get_db)):
    weather_reports_db = db.query(WeatherReport).filter(WeatherReport.land_id == id).all()  
    if weather_reports_db:
        return weather_reports_db
    raise HTTPException(status_code=404, detail="No weather reports found for this land")

