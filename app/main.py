from fastapi import FastAPI
from app.api.endpoints import news_analysis # Import the new router

app = FastAPI(title="NewsBot AI API") # Updated title to NewsBot

@app.get("/")
async def root():
    return {"message": "Welcome to the NewsBot AI API!"} # Updated welcome message

# Include routers
app.include_router(news_analysis.router)

# Further endpoints will be added via routers from app.api
# (The above comment can be removed or kept as desired)
