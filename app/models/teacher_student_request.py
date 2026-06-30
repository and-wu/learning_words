from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.request_status import RequestStatus
from app.enums.request_type import RequestType

from sqlalchemy import Enum as SQLEnum


class TeacherStudentRequest(Base):
    __tablename__ = "teacher_student_requests"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    from_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable = False
    )

    to_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable=False
    )

    request_type: Mapped[RequestType] = mapped_column(
        SQLEnum(
            RequestType,
            name="request_type",
        ),
        nullable=False
    )

    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(
            RequestStatus,
            name="request_status",
        ),
        server_default = RequestStatus.PENDING.value
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )