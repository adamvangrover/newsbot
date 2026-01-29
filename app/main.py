from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import news_analysis, reports, analysis, reasoning, system, federated, plugins
import os
import asyncio
from app.core.async_utils import task_manager
from app.services.federated_learning_service import fl_service
from app.core.plugin_manager import plugin_manager

app = FastAPI(title="NewsBot AI API")

@app.on_event("startup")
async def startup_event():
    # Load Plugins
    plugin_manager.load_plugins()

    # Start a background task to simulate activity for the dashboard
    async def heartbeat():
        while True:
            await asyncio.sleep(60)

    await task_manager.start_task("system_heartbeat", heartbeat())

    # Auto-start FL service for demo purposes
    await fl_service.start_training()

# Mount output directory to serve reports
app.mount("/output", StaticFiles(directory="output"), name="output")

# Include routers
app.include_router(news_analysis.router)
app.include_router(reports.router)
app.include_router(analysis.router)
app.include_router(reasoning.router, prefix="/api/reasoning", tags=["reasoning"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(federated.router, prefix="/api/federated", tags=["federated"])
app.include_router(plugins.router, prefix="/api/plugins", tags=["plugins"])

# Serve React Frontend
# 1. Mount assets
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# 2. Serve index.html for root and unknown paths (SPA routing)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Check if file exists in dist (e.g. favicon.ico)
    if os.path.exists(f"frontend/dist/{full_path}") and full_path != "":
        return FileResponse(f"frontend/dist/{full_path}")

    # Otherwise return index.html
    return FileResponse("frontend/dist/index.html")
