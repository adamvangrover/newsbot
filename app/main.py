from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import news_analysis, reports, analysis, reasoning
import os

app = FastAPI(title="NewsBot AI API")

# Mount output directory to serve reports
app.mount("/output", StaticFiles(directory="output"), name="output")

# Include routers
app.include_router(news_analysis.router)
app.include_router(reports.router)
app.include_router(analysis.router)
app.include_router(reasoning.router, prefix="/api/reasoning", tags=["reasoning"])

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
