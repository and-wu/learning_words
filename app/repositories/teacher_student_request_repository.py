from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from app.models.teacher_student_requests import TeacherStudentRequest
from app.enums.request_status import RequestStatus

class TeacherStudentRequestRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, request: TeacherStudentRequest) -> TeacherStudentRequest:
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)

        return request

    def get_by_id(self, request_id: int) -> TeacherStudentRequest | None:
        stmt = (
            select(TeacherStudentRequest)
            .where(TeacherStudentRequest.id == request_id)
        )

        return self.db.scalar(stmt)

    def get_pending_between_users(
            self,
            user1_id: int,
            user2_id: int,
    ) -> TeacherStudentRequest | None:
        stmt = (
            select(TeacherStudentRequest)
            .where(
                or_(
                    and_(
                        TeacherStudentRequest.from_user_id == user1_id,
                        TeacherStudentRequest.to_user_id == user2_id,
                    ),
                    and_(
                        TeacherStudentRequest.from_user_id == user2_id,
                        TeacherStudentRequest.to_user_id == user1_id,
                    ),
                ),
                TeacherStudentRequest.status == RequestStatus.PENDING,
            )
        )

        return self.db.scalar(stmt)

    def get_incoming(self, user_id: int) -> list[TeacherStudentRequest]:
        stmt = (
            select(TeacherStudentRequest)
            .where(
                TeacherStudentRequest.to_user_id == user_id,
            )
            .order_by(
                TeacherStudentRequest.created_at.desc(),
            )
        )

        return self.db.scalars(stmt).all()

    def get_outgoing(self, user_id: int) -> list[TeacherStudentRequest]:
        stmt = (
            select(TeacherStudentRequest)
            .where(
                TeacherStudentRequest.from_user_id == user_id,
            )
            .order_by(
                TeacherStudentRequest.created_at.desc(),
            )
        )

        return self.db.scalars(stmt).all()

    def update(self, request: TeacherStudentRequest) -> TeacherStudentRequest:

        self.db.add(request)
        self.db.flush()
        self.db.commit()
        self.db.refresh(request)

        return request