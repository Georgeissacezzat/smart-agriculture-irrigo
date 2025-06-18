from fastapi import APIRouter
from src.routes.user_routes import router as user_router
from src.routes.land_routes import router as land_router
from src.routes.soil_routes import router as soil_router
from src.routes.weather_routes import router as weather_router
from src.routes.irrigation_decision_routes import router as irrigation_router
from src.routes.test_route import router as test_router


smart_agriculture = APIRouter()


smart_agriculture.include_router(user_router, prefix="/users", tags=["Users"])
smart_agriculture.include_router(land_router, prefix="/lands", tags=["Lands"])
smart_agriculture.include_router(soil_router, prefix="/soil", tags=["Soil"])
smart_agriculture.include_router(weather_router, prefix="/weather", tags=["Weather"])
smart_agriculture.include_router(irrigation_router, prefix="/irrigation", tags=["Irrigation"])
smart_agriculture.include_router(test_router, prefix="/test", tags=["Testing"])