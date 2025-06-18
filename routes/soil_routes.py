from fastapi import status, Depends , APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.models import SoilReport 
from src.schemas import SoilReportSchema
from src.database import get_db


router = APIRouter()


@router.get("/get-latest-soil-report/{id}")
async def get_latest_soil_report (id : int , db : Session = Depends(get_db)) -> dict :
    latest_report = (
        db.query(SoilReport)
        .filter(SoilReport.land_id == id)  
        .order_by(SoilReport.timestamp.desc()) 
        .first()
    )
    if latest_report :
        return{
            "report_id" : latest_report.report_id , 
            "land_id" : latest_report.land_id , 
            "timestamp" : latest_report.timestamp , 
            "t10" : latest_report.t10 , 
            "moisture" : latest_report.moisture ,    
            "t0" : latest_report.t0 
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Report found")


@router.get("/get-soil-reports/{id}" , response_model=List[SoilReportSchema])
async def get_soil_reports(id: int, db: Session = Depends(get_db)):
    soil_reports_db = db.query(SoilReport).filter(SoilReport.land_id == id).all()  
    if soil_reports_db:
        return soil_reports_db
    raise HTTPException(status_code=404, detail="No soil reports found for this land")