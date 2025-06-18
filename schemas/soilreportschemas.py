from datetime import datetime
from pydantic import BaseModel


class SoilReportSchema(BaseModel):
    report_id : int
    land_id : int 
    timestamp : datetime 
    t10 : float  
    moisture : float   
    t0 : float