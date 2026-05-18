import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Database import initDB
from Routes import router

# Frontend-URL aus Env, mit Dev-Fallback (Frontend läuft per compose.yaml auf Port 8000)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8000")


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    yield


app = FastAPI(title="LazyCook", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],  # Explizite Origins erforderlich mit allow_credentials=True
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.include_router(router)
