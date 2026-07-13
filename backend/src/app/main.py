from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.redis import redis
from app.core.qdrant import qdrant
from app.core.storage import storage

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

@app.get("/health/storage")
def storage_health():
    storage.client.head_bucket(Bucket=storage.bucket)
    return {"status": "healthy"}
@app.get("/health/qdrant")
def qdrant_health():
    return {
        "collections": qdrant.get_collections().collections
    }

@app.get("/health/redis")
def redis_health():
    redis.ping()
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"status": "Backend running"}