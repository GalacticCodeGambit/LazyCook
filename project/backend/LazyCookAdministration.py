from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Database import initDB
from Routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    yield


app = FastAPI(title="LazyCook", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
