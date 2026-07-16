from datetime import UTC, datetime, timedelta
from unittest import TestCase
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine, select

from app.api.auth import router as auth_router
from app.api.deps import AUTH_COOKIE_NAME
from app.core.database import get_session
from app.core.security import create_access_token, verify_access_token
from app.models.user import User
from app.schemas.auth import GoogleUserInfo
from app.services.auth_service import AuthService


def build_test_app(engine):
    app = FastAPI()
    app.include_router(auth_router)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return app


def create_test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    User.metadata.create_all(engine, tables=[User.__table__])
    return engine


class JWTTests(TestCase):
    def test_generate_and_verify_token(self):
        token = create_access_token("user-123")
        payload = verify_access_token(token)

        self.assertEqual(payload["sub"], "user-123")
        self.assertIn("iat", payload)
        self.assertIn("exp", payload)

    def test_expired_token_is_rejected(self):
        token = create_access_token(
            "user-123",
            additional_claims={
                "exp": datetime.now(UTC) - timedelta(seconds=1),
            },
        )

        with self.assertRaises(HTTPException) as context:
            verify_access_token(token)

        self.assertEqual(context.exception.status_code, 401)

    def test_invalid_token_is_rejected(self):
        with self.assertRaises(HTTPException) as context:
            verify_access_token("not-a-jwt")

        self.assertEqual(context.exception.status_code, 401)


class AuthServiceTests(TestCase):
    def setUp(self):
        self.engine = create_test_engine()
        self.google_user = GoogleUserInfo(
            sub="google-123",
            email="test@example.com",
            name="Test User",
            picture="https://example.com/avatar.png",
            email_verified=True,
        )

    def test_create_user(self):
        with Session(self.engine) as session:
            user = AuthService.get_or_create_user(session, self.google_user)

            self.assertEqual(user.google_sub, self.google_user.sub)
            self.assertEqual(user.email, self.google_user.email)

    def test_reuse_existing_user(self):
        with Session(self.engine) as session:
            first = AuthService.get_or_create_user(session, self.google_user)
            second = AuthService.get_or_create_user(session, self.google_user)

            self.assertEqual(first.id, second.id)

    def test_prevent_duplicate_users(self):
        with Session(self.engine) as session:
            AuthService.get_or_create_user(session, self.google_user)
            AuthService.get_or_create_user(session, self.google_user)

            users = session.exec(select(User)).all()
            self.assertEqual(len(users), 1)

    def test_updates_existing_profile(self):
        with Session(self.engine) as session:
            AuthService.get_or_create_user(session, self.google_user)

            updated = self.google_user.model_copy(
                update={
                    "email": "updated@example.com",
                    "name": "Updated User",
                    "picture": "https://example.com/new-avatar.png",
                }
            )
            user = AuthService.get_or_create_user(session, updated)

            self.assertEqual(user.email, "updated@example.com")
            self.assertEqual(user.name, "Updated User")
            self.assertEqual(
                user.profile_picture,
                "https://example.com/new-avatar.png",
            )


class AuthRouteTests(TestCase):
    def setUp(self):
        self.engine = create_test_engine()
        self.app = build_test_app(self.engine)
        self.client = TestClient(self.app)
        self.google_payload = {
            "userinfo": {
                "sub": "google-123",
                "email": "test@example.com",
                "name": "Test User",
                "picture": "https://example.com/avatar.png",
                "email_verified": True,
            }
        }

    def test_google_login_redirects(self):
        redirect_response = RedirectResponse(
            url="https://accounts.google.com/o/oauth2/auth",
            status_code=302,
        )

        with patch(
            "app.api.auth.oauth.google.authorize_redirect",
            new=AsyncMock(return_value=redirect_response),
        ) as mocked_redirect:
            response = self.client.get("/auth/google/login", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["location"],
            "https://accounts.google.com/o/oauth2/auth",
        )
        mocked_redirect.assert_awaited_once()

    def test_callback_sets_cookie_and_redirects(self):
        with patch(
            "app.api.auth.oauth.google.authorize_access_token",
            new=AsyncMock(return_value=self.google_payload),
        ):
            response = self.client.get("/auth/google/callback", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("access_token=", response.headers["set-cookie"])
        self.assertIn("HttpOnly", response.headers["set-cookie"])
        self.assertIn("Path=/", response.headers["set-cookie"])
        self.assertIn("SameSite=lax", response.headers["set-cookie"])

    def test_callback_creates_or_reuses_user(self):
        with patch(
            "app.api.auth.oauth.google.authorize_access_token",
            new=AsyncMock(return_value=self.google_payload),
        ):
            self.client.get("/auth/google/callback", follow_redirects=False)
            self.client.get("/auth/google/callback", follow_redirects=False)

        with Session(self.engine) as session:
            users = session.exec(select(User)).all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].google_sub, "google-123")

    def test_auth_me_returns_authenticated_user(self):
        with patch(
            "app.api.auth.oauth.google.authorize_access_token",
            new=AsyncMock(return_value=self.google_payload),
        ):
            callback_response = self.client.get(
                "/auth/google/callback",
                follow_redirects=False,
            )

        cookie_header = callback_response.headers["set-cookie"]
        token = cookie_header.split(f"{AUTH_COOKIE_NAME}=", 1)[1].split(";", 1)[0]

        response = self.client.get(
            "/auth/me",
            cookies={AUTH_COOKIE_NAME: token},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@example.com")

    def test_auth_me_returns_401_without_cookie(self):
        response = self.client.get("/auth/me")
        self.assertEqual(response.status_code, 401)

    def test_auth_me_returns_401_with_invalid_cookie(self):
        response = self.client.get(
            "/auth/me",
            cookies={AUTH_COOKIE_NAME: "invalid-token"},
        )
        self.assertEqual(response.status_code, 401)

    def test_logout_clears_cookie(self):
        response = self.client.post("/auth/logout")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token=\"\"", response.headers["set-cookie"])
        self.assertIn("expires=", response.headers["set-cookie"].lower())

    def test_end_to_end_authentication_flow(self):
        with patch(
            "app.api.auth.oauth.google.authorize_access_token",
            new=AsyncMock(return_value=self.google_payload),
        ):
            callback_response = self.client.get(
                "/auth/google/callback",
                follow_redirects=False,
            )

        token = callback_response.headers["set-cookie"].split(
            f"{AUTH_COOKIE_NAME}=", 1
        )[1].split(";", 1)[0]

        me_response = self.client.get(
            "/auth/me",
            cookies={AUTH_COOKIE_NAME: token},
        )
        logout_response = self.client.post(
            "/auth/logout",
            cookies={AUTH_COOKIE_NAME: token},
        )
        post_logout_me_response = self.client.get("/auth/me")

        self.assertEqual(callback_response.status_code, 302)
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(post_logout_me_response.status_code, 401)
