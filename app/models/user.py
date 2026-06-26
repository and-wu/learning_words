from datetime import datetime

from sqlalchemy import BigInteger, Text, DateTime, Boolean, func, String, text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.base import Base
from app.enums.user_role import UserRole

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.session import Session

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    # email хранить только lowercase
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    login: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            name="user_role",
        ),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true")
    )

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )