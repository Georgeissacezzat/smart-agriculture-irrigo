from datetime import datetime
from pydantic import BaseModel


class WeatherReportSchema(BaseModel):
    report_id: int
    land_id: int
    timestamp: datetime
    temperature_2m: float
    relative_humidity_2m: float
    apparent_temperature: float
    is_day: int
    precipitation: float
    rain: float
    showers: float
    snowfall: float
    weather_code: int
    cloud_cover: int
    pressure_msl: float
    surface_pressure: float
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float