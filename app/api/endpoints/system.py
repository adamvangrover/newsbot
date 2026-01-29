from fastapi import APIRouter
from app.services.system_monitor import system_monitor
from app.core.async_utils import task_manager

router = APIRouter()

@router.get("/status")
async def get_system_status():
    return system_monitor.get_status()

@router.get("/tasks")
async def get_tasks():
    return task_manager.get_all_tasks()
