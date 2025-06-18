import asyncio
from fastapi import APIRouter
from src.utils import send_irrigation_emails_to_all
from src.data_collector import fetch_and_store_soil_data , fetch_and_store_weather_data
from src.ml import predict_irrigation_for_all_lands


router = APIRouter()


@router.get("/test")
async def test ():
    fetch_and_store_weather_data()
    await asyncio.sleep(1)
    fetch_and_store_soil_data()
    await asyncio.sleep(1)
    predict_irrigation_for_all_lands()
    await asyncio.sleep(1)
    send_irrigation_emails_to_all()