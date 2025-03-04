from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import UserNotFound
import logging


logger = logging.getLogger(__name__)


def add_expception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UserNotFound)
    async def handle_user_not_found_exception(request: Request, exc: UserNotFound):
        logger.error(f"Non-existent user_id: {exc.user_id} was requested")
        # raise HTTPException(status_code=404, detail=f"User does not exist") # also works for some reason
        return JSONResponse(status_code=404, content="User does not exist")

    return None
