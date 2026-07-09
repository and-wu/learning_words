from fastapi import APIRouter, Depends

from app.dependencies.services import get_student_word_service

from app.schemas.student_words import StudentWordResponse, AssignWordRequest, SelfAssignWordRequest
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.student_word_service import StudentWordService

router = APIRouter(
    prefix="/student_word",
    tags=["Student Word"],
)


@router.post("/assign",response_model=StudentWordResponse)
def assign_by_teacher(
        data: AssignWordRequest,
        current_user: User = Depends(get_current_user),
        service: StudentWordService = Depends(
            get_student_word_service,
        ),
):

    return service.assign_by_teacher(
        teacher=current_user,
        student_id=data.student_id,
        word_id=data.word_id,
    )

@router.post("/self", response_model=StudentWordResponse)
def assign_to_self(
    data: SelfAssignWordRequest,
    current_user: User = Depends(get_current_user),
    service: StudentWordService = Depends(
        get_student_word_service,
    ),
):

    return service.assign_to_self(
        student=current_user,
        word_id=data.word_id,
    )

@router.get("/", response_model=list[StudentWordResponse])
def get_student_words(
    current_user: User = Depends(get_current_user),
    service: StudentWordService = Depends(
        get_student_word_service,
    ),
):

    return service.get_student_words(
        current_user=current_user,
    )

@router.delete("/{student_word_id}")
def remove(
    student_word_id: int,
    current_user: User = Depends(get_current_user),
    service: StudentWordService = Depends(
        get_student_word_service,
    ),
):

    service.remove(
        current_user=current_user,
        student_word_id=student_word_id,
    )

    return {
        "message": "Word removed successfully",
    }