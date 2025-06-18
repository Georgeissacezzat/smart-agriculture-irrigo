from pydantic import BaseModel
from typing import Optional


class Create_Land (BaseModel):
    lat : float
    lon : float
    crop_type : str
    crop_days : int
    soil_type : str
    user_id : int

class Update_Land(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    crop_type: Optional[str] = None
    crop_days : Optional[int] = None
    soil_type : Optional[str] = None

class LandSchema(BaseModel):
    land_id: int
    lat: float
    lon: float
    crop_type: str
    crop_days : int
    soil_type : str