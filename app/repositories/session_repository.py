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
        self.db.commit()
        self.db.refresh(session)

        return session