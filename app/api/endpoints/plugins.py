from fastapi import APIRouter
from pydantic import BaseModel
from app.core.plugin_manager import plugin_manager

router = APIRouter()

class PluginToggle(BaseModel):
    name: str
    enabled: bool

@router.get("/")
async def list_plugins():
    return plugin_manager.get_plugins()

@router.post("/toggle")
async def toggle_plugin(payload: PluginToggle):
    success = plugin_manager.toggle_plugin(payload.name, payload.enabled)
    return {"success": success, "plugins": plugin_manager.get_plugins()}
