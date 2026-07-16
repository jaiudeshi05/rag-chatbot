from pathlib import Path
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parents[3]

PRIVATE_KEY = (
    BASE_DIR / settings.JWT_PRIVATE_KEY_PATH
).read_text(encoding="utf-8")

PUBLIC_KEY = (
    BASE_DIR / settings.JWT_PUBLIC_KEY_PATH
).read_text(encoding="utf-8")

def create_access_token(
    subject: str,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(UTC)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(days=settings.JWT_EXPIRE_DAYS),
    }

    if additional_claims:
        payload.update(additional_claims)

    token = jwt.encode(
        claims=payload,
        key=PRIVATE_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def verify_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token=token,
            key=PUBLIC_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except HTTPException:
        raise
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
