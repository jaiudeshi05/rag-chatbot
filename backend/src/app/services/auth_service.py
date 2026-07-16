from sqlmodel import Session, select

from app.models.user import User
from app.schemas.auth import GoogleUserInfo


class AuthService:
    @staticmethod
    def get_or_create_user(
        session: Session,
        google_user: GoogleUserInfo,
    ) -> User:
        user = session.exec(
            select(User).where(User.google_sub == google_user.sub)
        ).first()

        if user is None:
            user = User(
                google_sub=google_user.sub,
                email=google_user.email,
                name=google_user.name,
                profile_picture=google_user.picture,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

        profile_changed = False

        if user.email != google_user.email:
            user.email = google_user.email
            profile_changed = True

        if user.name != google_user.name:
            user.name = google_user.name
            profile_changed = True

        if user.profile_picture != google_user.picture:
            user.profile_picture = google_user.picture
            profile_changed = True

        if profile_changed:
            session.add(user)
            session.commit()
            session.refresh(user)

        return user
