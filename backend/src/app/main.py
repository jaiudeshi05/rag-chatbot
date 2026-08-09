from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.redis import redis
from app.core.qdrant import qdrant
from app.core.security import PRIVATE_KEY
from app.core.storage import storage
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.projects import router as projects_router
from app.api.documents import router as documents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(documents_router)
app.add_middleware(
    SessionMiddleware,
    secret_key=PRIVATE_KEY,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
