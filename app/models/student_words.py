from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.source_type import SourceType


class StudentWord(Base):
    __tablename__ = "student_words"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "word_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    word_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "words.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    assigned_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    source_type: Mapped[SourceType] = mapped_column(
        SQLEnum(
            SourceType,
            name="source_type",
        ),
        nullable=False,
    )

    correct_streak: Mapped[int] = mapped_column(
        Integer,
        server_default="0",
        nullable=False,
    )

    wrong_count: Mapped[int] = mapped_column(
        Integer,
        server_default="0",
        nullable=False,
    )

    last_result: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    last_review_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    next_review_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    interval_days: Mapped[int] = mapped_column(
        Integer,
        server_default="0",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )