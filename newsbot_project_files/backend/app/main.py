from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from newsbot_project_files.backend.app.core.config import settings
from newsbot_project_files.backend.app.api.v1.endpoints import company as company_v1
from newsbot_project_files.backend.app.api.v1.endpoints import market as market_v1
from newsbot_project_files.backend.app.api.v1.endpoints import tools as tools_v1 # Import the new tools router
from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
# Adjust origins as necessary for your frontend URL in production
origins = [
    "http://localhost",
    "http://localhost:3000", # Common React dev port
    "http://localhost:5173", # Common Vite dev port
    # Add your deployed frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], # Allow all standard methods
    allow_headers=["*"], # Allow all headers
)

# Include API routers
app.include_router(company_v1.router, prefix=settings.API_V1_STR, tags=["Company Analysis"])
app.include_router(market_v1.router, prefix=f"{settings.API_V1_STR}/market", tags=["Market Outlook"])
app.include_router(tools_v1.router, prefix=f"{settings.API_V1_STR}/tools", tags=["Utility Tools"]) # Add tools router

@app.on_event("startup")
async def startup_event():
    logger.info("NewsBot API starting up...")
    # You can add other startup logic here, like connecting to a database

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("NewsBot API shutting down...")
    # Add shutdown logic here, like closing database connections

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

# For debugging: list routes
# from fastapi.routing import APIRoute
# for route in app.routes:
#     if isinstance(route, APIRoute):
#         logger.debug(f"Route: {route.path} Methods: {route.methods} Name: {route.name}")
