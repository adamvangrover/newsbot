from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import news_analysis, reports
import os

app = FastAPI(title="NewsBot AI API")

# Mount frontend directory to serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Mount output directory to serve reports
app.mount("/output", StaticFiles(directory="output"), name="output")

# Mount components directory to serve markdown files
app.mount("/components", StaticFiles(directory="frontend/components"), name="components")

@app.get("/")
async def root():
    # Return the index.html from frontend
    return FileResponse('frontend/index.html')

# Include routers
app.include_router(news_analysis.router)
app.include_router(reports.router)
