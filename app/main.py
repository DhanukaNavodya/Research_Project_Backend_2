from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import mood_routes

app = FastAPI(title="Children Mental Health API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mood_routes.router)
