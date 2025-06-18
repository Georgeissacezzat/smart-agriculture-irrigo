from datetime import datetime
from pydantic import BaseModel


class IrrigationDecisionSchema(BaseModel):
    decision_id: int
    timestamp: datetime
    water_amount : float
    land_id: int