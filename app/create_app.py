from fastapi import FastAPI
from app import create_user_router
from app.exception_handlers import add_exception_handlers
from app.clients.db import DatabaseClient
from app.config import Config
from contextlib import asynccontextmanager

def create_application() -> FastAPI:

    config = Config()
    tables = ["user", "liked_post"]
    database_client = DatabaseClient(config, tables)

    user_router = create_user_router(database_client)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await database_client.connect()
        yield
        await database_client.disconnect()
    
    app = FastAPI(lifespan=lifespan)
    app.include_router(user_router)
    #  add user_router to the main application
    add_exception_handlers(app=app)

    return app