from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.student_words_repository import StudentWordRepository
from app.repositories.word_repository import WordRepository
from app.schemas.student_words import StudentWordResponse, AssignWordRequest, SelfAssignWordRequest
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository
from app.services.student_word_service import StudentWordService

router = APIRouter(
    prefix="/student_word",
    tags=["Student Word"],
)


@router.post("/assign",response_model=StudentWordResponse)
def assign_by_teacher(
        data: AssignWordRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    word_repository = WordRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)
    student_word_repository = StudentWordRepository(db)

    service = StudentWordService(
        user_repository=user_repository,
        word_repository=word_repository,
        teacher_student_repository=teacher_student_repository,
        student_word_repository=student_word_repository,
    )

    return service.assign_by_teacher(
        teacher=current_user,
        student_id=data.student_id,
        word_id=data.word_id,
    )

@router.post("/self", response_model=StudentWordResponse)
def assign_to_self(
    data: SelfAssignWordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user_repository = UserRepository(db)
    word_repository = WordRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)
    student_word_repository = StudentWordRepository(db)

    service = StudentWordService(
        user_repository=user_repository,
        word_repository=word_repository,
        teacher_student_repository=teacher_student_repository,
        student_word_repository=student_word_repository,
    )

    return service.assign_to_self(
        student=current_user,
        word_id=data.word_id,
    )

@router.get("/", response_model=list[StudentWordResponse])
def get_student_words(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user_repository = UserRepository(db)
    word_repository = WordRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)
    student_word_repository = StudentWordRepository(db)

    service = StudentWordService(
        user_repository=user_repository,
        word_repository=word_repository,
        teacher_student_repository=teacher_student_repository,
        student_word_repository=student_word_repository,
    )

    return service.get_student_words(
        current_user=current_user,
    )

@router.delete("/{student_word_id}")
def remove(
    student_word_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user_repository = UserRepository(db)
    word_repository = WordRepository(db)
    teacher_student_repository = TeacherStudentRepository(db)
    student_word_repository = StudentWordRepository(db)

    service = StudentWordService(
        user_repository=user_repository,
        word_repository=word_repository,
        teacher_student_repository=teacher_student_repository,
        student_word_repository=student_word_repository,
    )

    service.remove(
        current_user=current_user,
        student_word_id=student_word_id,
    )

    return {
        "message": "Word removed successfully",
    }