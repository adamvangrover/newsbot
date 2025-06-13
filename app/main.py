from fastapi import FastAPI

app = FastAPI(title="AI Company Analyzer API")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Company Analyzer API!"}

# Further endpoints will be added via routers from app.api
