from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import UserNotFound, UserAlreadyExist
import logging
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFound)
    async def handle_user_not_found_exception(request: Request, exc: UserNotFound):
        logger.error(f"Non-existent user_id: {exc.user_id} was requested")
        # raise HTTPException(status_code=404, detail=f"User does not exist") # also works for some reason
        return JSONResponse(status_code=404, content="User does not exist")

    @app.exception_handler(UserAlreadyExist)
    async def handle_user_already_exists_exception(
        request: Request, exc: UserAlreadyExist
    ):
        logger.error("Tried to add a user that already exists.")
        # raise HTTPException(status_code=404, detail=f"User does not exist") # also works for some reason
        return JSONResponse(status_code=400, content="User already exists")

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError):
        logger.error("Encountered integrity error when inserting user")
        return JSONResponse(
            status_code=400, content="User conflicts with existing user"
        )

    return None