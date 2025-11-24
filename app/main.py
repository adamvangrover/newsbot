from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import news_analysis # Import the new router
import os

app = FastAPI(title="NewsBot AI API") # Updated title to NewsBot

# Mount frontend directory to serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    # Return the index.html from frontend
    return FileResponse('frontend/index.html')

# Include routers
app.include_router(news_analysis.router)
