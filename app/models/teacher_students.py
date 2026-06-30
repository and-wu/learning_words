from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, func, DateTime, Boolean, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TeacherStudent(Base):
    __tablename__ = "teacher_students"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    teacher_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable=False
    )

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true")
    )

    __table_args__ = (
        UniqueConstraint(
            "teacher_id",
            "student_id",
        ),
    )