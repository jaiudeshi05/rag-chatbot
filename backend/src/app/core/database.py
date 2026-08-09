import socket
from typing import Iterator
from urllib.parse import urlparse

import app.models
from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


database_url = urlparse(settings.DATABASE_URL)

if not database_url.hostname:
    raise RuntimeError("DATABASE_URL does not contain a valid database hostname")

database_host = database_url.hostname
database_port = database_url.port or 5432


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


@event.listens_for(engine, "do_connect")
def set_ipv4_hostaddr(dialect, conn_rec, cargs, cparams):
    try:
        addresses = socket.getaddrinfo(
            database_host,
            database_port,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )

        if addresses:
            cparams["hostaddr"] = addresses[0][4][0]

    except socket.gaierror:
        # Let libpq/psycopg2 resolve the hostname normally.
        # This prevents a temporary lack of an IPv4 DNS record
        # from preventing application startup.
        pass


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session