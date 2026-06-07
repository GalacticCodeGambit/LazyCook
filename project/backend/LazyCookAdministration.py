import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.Database import initDB
from routes.AuthRoutes import router as auth_router
from routes.UserRoutes import router as users_router
from routes.RecipeRoutes import router as recipes_router

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8000")


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    yield


app = FastAPI(title="LazyCook", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(recipes_router)
