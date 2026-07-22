from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.enums.user_role import UserRole
from app.models.user import User


def get_current_student(
        current_user: User = Depends(get_current_user)
) -> User:

    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access student statistics",
        )

    return current_user
