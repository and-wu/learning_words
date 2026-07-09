from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.repositories.word_repository import WordRepository
from app.repositories.student_words_repository import StudentWordRepository
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository

from app.services.word_service import WordService
from app.services.student_word_service import StudentWordService
from app.services.exercise_service import ExerciseService
from app.services.teacher_student_service import TeacherStudentService

def get_word_service(
    db: Session = Depends(get_db),
) -> WordService:

    return WordService(
        word_repository=WordRepository(db),
    )

def get_teacher_student_service(
    db: Session = Depends(get_db),
) -> TeacherStudentService:

    return TeacherStudentService(
        user_repository=UserRepository(db),
        teacher_student_repository=TeacherStudentRepository(db),
    )

def get_exercise_service(
    db: Session = Depends(get_db),
) -> ExerciseService:

    return ExerciseService(
        exercise_result_repository=ExerciseResultRepository(db),
        student_word_repository=StudentWordRepository(db),
        word_repository=WordRepository(db),
    )

