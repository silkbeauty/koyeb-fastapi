import os
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

import motor.motor_asyncio

from app.routes import router 


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URI"))
    db = client["bookdb"]
    app.state.db = db

    yield  # This represents the running FastAPI app

    client.close()


def create_app():
    app = FastAPI(
        title="FastAPI Title",
        version="1.2.1",
        docs_url="/",
        description="DESCRIPTION",
        lifespan=lambda app: lifespan(app)
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