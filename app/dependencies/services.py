from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.repositories.session_repository import SessionRepository
from app.repositories.teacher_student_request_repository import TeacherStudentRequestRepository
from app.repositories.word_repository import WordRepository
from app.repositories.student_word_repository import StudentWordRepository
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository

from app.services.auth_service import AuthService
from app.services.exercises.factory import ExerciseHandlerFactory
from app.services.student_statistics_service import StudentStatisticsService
from app.services.teacher_dashboard_service import TeacherDashboardService
from app.services.teacher_student_request_service import TeacherStudentRequestService
from app.services.word_service import WordService
from app.services.student_word_service import StudentWordService
from app.services.exercise_service import ExerciseService
from app.services.teacher_student_service import TeacherStudentService

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:

    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    return AuthService(
        user_repository=user_repository,
        session_repository=session_repository,
    )

def get_student_word_service(db: Session = Depends(get_db)) -> StudentWordService:

    return StudentWordService(
        user_repository=UserRepository(db),
        word_repository=WordRepository(db),
        teacher_student_repository=TeacherStudentRepository(db),
        student_word_repository=StudentWordRepository(db),
    )

def get_word_service(db: Session = Depends(get_db)) -> WordService:

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

def get_teacher_student_request_service(
    db: Session = Depends(get_db),
) -> TeacherStudentRequestService:

    return TeacherStudentRequestService(
        user_repository=UserRepository(db),
        teacher_student_repository=TeacherStudentRepository(db),
        teacher_student_request_repository=TeacherStudentRequestRepository(db),
    )

def get_exercise_service(db: Session = Depends(get_db)) -> ExerciseService:

    word_repository = WordRepository(db)

    exercise_handler_factory = ExerciseHandlerFactory(
        word_repository=word_repository,
    )

    return ExerciseService(
        exercise_result_repository=ExerciseResultRepository(db),
        student_word_repository=StudentWordRepository(db),
        word_repository=word_repository,
        exercise_handler_factory=exercise_handler_factory,
    )

# Создает сервис статистики ученика
def get_student_statistics_service(
    db: Session = Depends(get_db),
) -> StudentStatisticsService:

    return StudentStatisticsService(
        student_word_repository=StudentWordRepository(db),
        exercise_result_repository=ExerciseResultRepository(db),
    )

# Создает сервис кабинета преподавателя
def get_teacher_dashboard_service(
    db: Session = Depends(get_db),
) -> TeacherDashboardService:

    return TeacherDashboardService(
        user_repository=UserRepository(db),
        teacher_student_repository=TeacherStudentRepository(db),
        student_word_repository=StudentWordRepository(db),
        exercise_result_repository=ExerciseResultRepository(db),
    )