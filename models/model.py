from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from src.database import Base, engine

class User(Base):
    __tablename__ = 'users'  
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password = Column(String, nullable=False) 
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    lands = relationship("Land", back_populates="owner", cascade="all, delete-orphan")

class Land(Base):
    __tablename__ = "lands"

    land_id = Column(Integer, primary_key=True, autoincrement=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    crop_type = Column(Integer, nullable=False)
    crop_days = Column(Integer, nullable=False)
    soil_type = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="lands")
    soil_reports = relationship("SoilReport", back_populates="land", cascade="all, delete-orphan")
    weather_reports = relationship("WeatherReport", back_populates="land", cascade="all, delete-orphan")
    irrigation_decisions = relationship("IrrigationDecision", back_populates="land", cascade="all, delete-orphan")

class SoilReport(Base):
    __tablename__ = "soil_reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)  # Added an ID for simpler queries
    land_id = Column(Integer, ForeignKey("lands.land_id", ondelete="CASCADE"))
    timestamp = Column(TIMESTAMP, default=func.now(), nullable=False)
    t10 = Column(Float, nullable=False)
    moisture = Column(Float, nullable=False)
    t0 = Column(Float, nullable=False)

    land = relationship("Land", back_populates="soil_reports")

class WeatherReport(Base):
    __tablename__ = "weather_reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)  # Added an ID
    land_id = Column(Integer, ForeignKey("lands.land_id", ondelete="CASCADE"))
    timestamp = Column(TIMESTAMP, default=func.now(), nullable=False)
    temperature_2m = Column(Float, nullable=False)
    relative_humidity_2m = Column(Float, nullable=False)
    apparent_temperature = Column(Float, nullable=False)
    is_day = Column(Integer, nullable=False)
    precipitation = Column(Float, nullable=False)
    rain = Column(Float, nullable=False)
    showers = Column(Float, nullable=False)
    snowfall = Column(Float, nullable=False)
    weather_code = Column(Integer, nullable=False)
    cloud_cover = Column(Integer, nullable=False)
    pressure_msl = Column(Float, nullable=False)
    surface_pressure = Column(Float, nullable=False)
    wind_speed_10m = Column(Float, nullable=False)
    wind_direction_10m = Column(Integer, nullable=False)
    wind_gusts_10m = Column(Float, nullable=False)

    land = relationship("Land", back_populates="weather_reports")

class IrrigationDecision(Base):
    __tablename__ = "irrigation_decisions"

    decision_id = Column(Integer, primary_key=True, autoincrement=True)  
    timestamp = Column(TIMESTAMP, default=func.now(), nullable=False)
    water_amount = Column(Float, nullable=False)
    land_id = Column(Integer, ForeignKey("lands.land_id", ondelete="CASCADE"), nullable=False)

    land = relationship("Land", back_populates="irrigation_decisions")

Base.metadata.create_all(engine)
