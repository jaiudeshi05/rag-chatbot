from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.api.deps import AUTH_COOKIE_NAME, get_current_user
from app.core.config import settings
from app.core.database import get_session
from app.core.oauth import oauth
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import AuthenticatedUserResponse, GoogleUserInfo
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

COOKIE_MAX_AGE = settings.JWT_EXPIRE_DAYS * 24 * 60 * 60


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request=request,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    session: Session = Depends(get_session),
):
    token = await oauth.google.authorize_access_token(request)
    google_user = GoogleUserInfo.model_validate(token["userinfo"])
    user = AuthService.get_or_create_user(session, google_user)
    access_token = create_access_token(subject=str(user.id))

    response = RedirectResponse(url=settings.FRONTEND_URL, status_code=302)
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=access_token,
        max_age=COOKIE_MAX_AGE,
        expires=COOKIE_MAX_AGE,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/me", response_model=AuthenticatedUserResponse)
def get_authenticated_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key=AUTH_COOKIE_NAME,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        path="/",
    )
    return {"message": "Logged out successfully"}
