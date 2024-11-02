from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi import FastAPI, Depends, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.app.db.postge_session import get_db, engine, Base, AsyncSessionLocal
from src.app.api.v1.routes import parcels
from src.app.db.init_data import init_parcel_types
from src.app.services.user_session_service import create_session, extend_session, get_session_data, session_exists
from src.app.db.redis_session import redis_client
from src.app.utils.logging_config import LOGGING_CONFIG
import logging


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await init_parcel_types(session)

    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    logger.info('Root endpoint accessed')
    return {"message": "Welcome to the Pochta Rossii API"}

app.include_router(parcels.router, prefix="/parcels", tags=["parcels"])

@app.get("/healthcheck")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@app.middleware("http")
async def manage_session(request: Request, call_next):
    session_id = request.cookies.get("session_id")

    if session_id and await session_exists(session_id):
        await extend_session(session_id)
        response = await call_next(request)
    else:
        session_id = str(uuid4())
        initial_session_data = "Initial session data"
        await create_session(session_id, initial_session_data)
        response = Response("Session established", status_code=200)
        response.set_cookie(key="session_id", value=session_id)

    return response


@app.get("/example")
async def example_endpoint(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        session_data = await get_session_data(session_id)
        if not session_data:
            session_data = "No data found for this session."
    else:
        session_data = "No session ID found."

    return {"session_id": session_id, "session_data": session_data}

def create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()