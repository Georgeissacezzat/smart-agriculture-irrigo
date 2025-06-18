from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.data_collector import (
    fetch_and_store_weather_data,
    fetch_and_store_soil_data,
)
from src.ml import predict_irrigation_for_all_lands
from src.utils import increase_crop_day , send_irrigation_emails_to_all


scheduler = BackgroundScheduler()  


def fetch_weather_soil_and_predict():
    db: Session = SessionLocal()
    fetch_and_store_weather_data()
    fetch_and_store_soil_data()
    time.sleep(10)  
    predict_irrigation_for_all_lands()  
    time.sleep(10)
    send_irrigation_emails_to_all()
    db.close()


def setup_jobs():
    scheduler.add_job(
        fetch_weather_soil_and_predict,
        CronTrigger(hour="0,12", minute=1),
        id="sequential_jobs",
        replace_existing=True,
    )
    scheduler.add_job(
        increase_crop_day,
        CronTrigger(hour=0, minute=0),
        id="increase_crop_days",
        replace_existing=True,
    )

def start_scheduler():
    if not scheduler.running:
        setup_jobs()
        scheduler.start()
        print("Scheduler started.")


def stop_scheduler():
    if scheduler.running:
        print("Shutting down scheduler...")
        scheduler.shutdown()


