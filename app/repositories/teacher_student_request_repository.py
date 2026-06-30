from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.teacher_student_requests import TeacherStudentRequests
from app.enums.request_status import RequestStatus

class TeacherStudentRequestRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, request: TeacherStudentRequests) -> TeacherStudentRequests:
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)

        return request

    def get_by_id(self, request_id: int) -> TeacherStudentRequests | None:
        stmt = (
            select(TeacherStudentRequests)
            .where(TeacherStudentRequests.id == request_id)
        )

        return self.db.scalar(stmt)

    def get_pending(self, from_user_id: int, to_user_id: int) -> TeacherStudentRequests | None:
        stmt = (
            select(TeacherStudentRequests)
            .where(
                TeacherStudentRequests.from_user_id == from_user_id,
                TeacherStudentRequests.to_user_id == to_user_id,
                TeacherStudentRequests.status == RequestStatus.PENDING,
            )
        )

        return self.db.scalar(stmt)

    def update(self, request: TeacherStudentRequests) -> TeacherStudentRequests:

        self.db.commit()
        self.db.refresh(request)

        return request