from fastapi import FastAPI
from app import create_user_router
from app.exception_handlers import add_expception_handlers


def create_application() -> FastAPI:
    user_router = create_user_router()

    app = FastAPI()
    app.include_router(user_router)
    #  add user_router to the main application
    add_expception_handlers(app=app)

    return app


app = create_application()
