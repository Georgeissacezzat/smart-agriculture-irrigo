from sqlalchemy import text
from datetime import datetime
from src.database import engine

def increase_crop_day():
    query = text("UPDATE lands SET crop_days = crop_days + 1")  # Fix column name
    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()
    print(f"crop_days updated successfully at {datetime.now()}")