from fastapi import status , Depends , APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.models import Land 
from src.schemas import  Create_Land , Update_Land , LandSchema 
from src.database import get_db
from src.utils import crop_mapping , reverse_crop_mapping , soil_type_mapping , reverse_soil_mapping


router = APIRouter()


@router.post("/create-land" , status_code = status.HTTP_201_CREATED)
async def create_land(land: Create_Land, db: Session = Depends(get_db)) -> dict:
    formatted_crop_type = land.crop_type.title()
    formatted_soil_type = land.soil_type.lower()

    if formatted_crop_type not in crop_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid crop type '{land.crop_type}'. Allowed types: {list(crop_mapping.keys())}"
        )
    
    if formatted_soil_type not in soil_type_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid crop type '{land.soil_type}'. Allowed types: {list(soil_type_mapping.keys())}"
        )

    mapped_crop_value = crop_mapping[formatted_crop_type]
    mapped_soil_value = soil_type_mapping[formatted_soil_type]

    new_land = Land(
        lat=land.lat,
        lon=land.lon,
        crop_type=mapped_crop_value,
        crop_days=land.crop_days,
        soil_type=mapped_soil_value,
        user_id=land.user_id
    )

    db.add(new_land)
    db.commit()
    db.refresh(new_land)

    return {"land_id": new_land.land_id}


@router.patch("/update-land/{id}")
async def update_land(id: int, land: Update_Land, db: Session = Depends(get_db)) -> dict:
    land_record = db.query(Land).filter(Land.land_id == id).first()
    
    if not land_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Land not found"
        )

    if land.lat is not None:
        land_record.lat = land.lat
    if land.lon is not None:
        land_record.lon = land.lon
    if land.crop_days is not None:
        land_record.crop_days = land.crop_days
    if land.crop_type is not None:
        formatted_crop_type = land.crop_type.title()
        if formatted_crop_type not in crop_mapping:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid crop type '{land.crop_type}'. Allowed types: {list(crop_mapping.keys())}"
            )
        land_record.crop_type = crop_mapping[formatted_crop_type]
    if land.soil_type is not None:
        formatted_soil_type = land.soil_type.lower()
        if formatted_soil_type not in soil_type_mapping:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid crop type '{land.soil_type}'. Allowed types: {list(soil_type_mapping.keys())}"
            )
        land_record.soil_type = soil_type_mapping[formatted_soil_type]

    db.commit()
    db.refresh(land_record)

    return {
        "land_id": land_record.land_id,
        "lat": land_record.lat,
        "lon": land_record.lon,
        "crop_type": reverse_crop_mapping[land_record.crop_type],
        "crop_days": land_record.crop_days,
        "soil_type": reverse_soil_mapping[land_record.soil_type],
        "user_id": land_record.user_id
    }


@router.delete("/delete-land/{id}")
async def delete_land (id : int , db : Session = Depends(get_db)):
    Land_check = db.query(Land).filter(Land.land_id == id).first()
    if Land_check :
        db.delete(Land_check)
        db.commit()
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Land not found")


@router.get("/get-user-lands/{id}", response_model=List[LandSchema])
async def get_user_lands(id: int, db: Session = Depends(get_db)):
    lands = db.query(Land).filter(Land.user_id == id).all()

    for land in lands:
        land.crop_type = reverse_crop_mapping.get(land.crop_type, "Unknown")
        land.soil_type = reverse_soil_mapping.get(land.soil_type, "Unknown")

    return lands


@router.get("/get-land/{id}")
async def get_land(id: int, db: Session = Depends(get_db)) -> dict:
    land_record = db.query(Land).filter(Land.land_id == id).first()

    if not land_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Land not found")

    return {
        "lat": land_record.lat,
        "lon": land_record.lon,
        "crop_type": reverse_crop_mapping.get(land_record.crop_type, "Unknown"),
        "crop_days": land_record.crop_days,
        "soil_type": reverse_soil_mapping.get(land_record.soil_type, "Unknown"),
        "user_id": land_record.user_id
    }
