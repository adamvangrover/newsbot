from fastapi import APIRouter
from app.services.federated_learning_service import fl_service

router = APIRouter()

@router.get("/status")
async def get_fl_status():
    return fl_service.get_status()

@router.post("/start")
async def start_fl():
    await fl_service.start_training()
    return {"message": "Training started"}

@router.post("/stop")
async def stop_fl():
    await fl_service.stop_training()
    return {"message": "Training stopped"}
