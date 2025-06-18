from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routes import smart_agriculture
from src.scheduler import start_scheduler, stop_scheduler

version = "v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()  
    yield
    stop_scheduler()  


app = FastAPI(
    title="IRRIGO",
    description="A REST API FOR IRRIGO APP SERVICE",
    version=version,
    lifespan=lifespan
)

app.include_router(smart_agriculture, prefix=f"/irrigo/{version}")