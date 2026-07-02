from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Text,
    func, String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    korean: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    translation: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    part_of_speech: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )