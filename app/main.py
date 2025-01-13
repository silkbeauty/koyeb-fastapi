from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

import motor.motor_asyncio

from app.config import Settings
from app.routes import router 

@asynccontextmanager
async def lifespan(app: FastAPI, settings:Settings) -> AsyncGenerator:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.CFG["MONGO_URI"])
    db = client[settings.CFG["MONGO_DB_NAME"]]
    app.state.db = db

    yield  # This represents the running FastAPI app

    client.close()


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/",
        description=settings.DESCRIPTION,
        lifespan=lambda app: lifespan(app, settings)
    )

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app