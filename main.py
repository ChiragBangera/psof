from fastapi import FastAPI
from app import create_user_router
from app.exception_handlers import add_expception_handlers


def create_application() -> FastAPI:
    profile_infos, users_content = get_profile_and_users_content()
    user_router = create_user_router(profile_infos, users_content)

    app = FastAPI()
    app.include_router(user_router)
    #  add user_router to the main application
    add_expception_handlers(app=app)

    return app


def get_profile_and_users_content():
    profile_infos = {
        0: {
            "short_description": "My bio description",
            "long_bio": "This is my longer bio",
        }
    }

    users_content = {0: {"liked_posts": [1] * 9}}

    return profile_infos, users_content


app = create_application()
