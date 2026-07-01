from datetime import datetime

import sqlalchemy as sa
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
        nullable = False,
        index=True
    )

    to_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    request_type: Mapped[RequestType] = mapped_column(
        SQLEnum(
            RequestType,
            values_callable=lambda enum: [e.value for e in enum],
            name="request_type"
        ),
        nullable=False
    )

    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(
            RequestStatus,
            values_callable=lambda enum: [e.value for e in enum],
            name="request_status"
        ),
        nullable = False,
        server_default = sa.text("'pending'"),
        default=RequestStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable = False
    )

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )