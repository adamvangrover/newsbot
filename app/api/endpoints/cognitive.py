from fastapi import APIRouter
from app.services.cognitive_service import cognitive_service

router = APIRouter()

@router.on_event("startup")
async def startup_cognitive():
    await cognitive_service.start_all()

@router.get("/agents")
async def get_agents():
    return cognitive_service.get_agent_status()

@router.get("/evolution")
async def get_evolution():
    return cognitive_service.get_evolution_status()
