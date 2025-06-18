from fastapi import Depends , APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.models import IrrigationDecision
from src.schemas import IrrigationDecisionSchema
from src.database import get_db


router = APIRouter()


@router.get("/get-irrigation-decisions/{id}" ,response_model=List[IrrigationDecisionSchema])
async def get_irrigation_decisions(id : int , db: Session = Depends(get_db)):
    irrigation_decisions = (
        db.query(IrrigationDecision)
        .filter(IrrigationDecision.land_id == id)
        .all()
    )
    if irrigation_decisions:
        return irrigation_decisions
    raise HTTPException(status_code=404, detail="No irrigation decisions found for this land ID")