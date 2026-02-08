from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable


def add_exception_handlers(app: FastAPI) -> None:
    """Add standardized exception handlers to the FastAPI app"""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "code": exc.status_code
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "code": 500
            }
        )