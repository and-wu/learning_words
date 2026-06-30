from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.session import Session as UserSession


class SessionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        session: UserSession,
    ) -> UserSession:

        self.db.add(session)
        self.db.flush()
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_by_token(
            self,
            token: str,
    ) -> UserSession | None:
        stmt = (
            select(UserSession)
            .where(UserSession.session_token == token)
        )

        return self.db.scalar(stmt)

    def delete(
            self,
            session: UserSession,
    ) -> None:
        self.db.delete(session)
        self.db.commit()