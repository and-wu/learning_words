from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.exercise_type import ExerciseType


class ExerciseResult(Base):
    __tablename__ = "exercise_results"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
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

    exercise_type: Mapped[ExerciseType] = mapped_column(
        SQLEnum(
            ExerciseType,
            values_callable=lambda enum: [e.value for e in enum],
            name="exercise_type",
        ),
        nullable=False,
    )

    correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    response: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    word: Mapped["Word"] = relationship(
        foreign_keys=[word_id],
    )

    user: Mapped["User"] = relationship(
        foreign_keys=[user_id],
    )
