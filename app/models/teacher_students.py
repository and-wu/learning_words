from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, func, DateTime, Boolean, text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TeacherStudents(Base):
    __tablename__ = "teacher_students"

    __table_args__ = (
        UniqueConstraint("teacher_id", "student_id"),

        # 👇 ДОПОЛНИТЕЛЬНО: можно добавить составной индекс
        # если часто ищешь пары teacher+student
        Index("ix_teacher_students_teacher_id", "teacher_id"),
        Index("ix_teacher_students_student_id", "student_id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    teacher_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id",
                   ondelete="CASCADE"),
        nullable=False,
        index=True
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

