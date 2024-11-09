from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.app.utils.logging_config import logger
from src.app.exceptions import ParcelNotFoundException, UnauthorizedException

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def parcel_not_found_exception_handler(request: Request, exc: ParcelNotFoundException) -> JSONResponse:
    logger.warning(f"Parcel not found: {exc}")
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    logger.warning(f"Unauthorized access attempt: {exc}")
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )