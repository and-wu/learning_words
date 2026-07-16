from fastapi import HTTPException, status

from app.models import StudentWord, ExerciseResult
from app.models.user import User
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.student_word_repository import StudentWordRepository
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.teacher_dashboard import StudentDashboardResponse, StudentDashboardDetailsResponse, \
    StudentWordProgressResponse, StudentHistoryResponse, ExerciseHistoryResponse

class TeacherDashboardService:

    def __init__(
        self,
        user_repository: UserRepository,
        teacher_student_repository: TeacherStudentRepository,
        student_word_repository: StudentWordRepository,
        exercise_result_repository: ExerciseResultRepository,
    ):
        self.user_repository = user_repository
        self.teacher_student_repository = teacher_student_repository
        self.student_word_repository = student_word_repository
        self.exercise_result_repository = exercise_result_repository

    # ==========================================================
    # Public methods
    # ==========================================================

    # Возвращает список учеников преподавателя с краткой статистикой
    def get_students_dashboard(self, current_user: User,) -> list[StudentDashboardResponse]:

        students = self.teacher_student_repository.get_student_users(
            current_user.id,
        )

        return [
            self._build_student_dashboard(student)
            for student in students
        ]

    # Возвращает подробную информацию по ученику
    def get_student_dashboard(self, current_user: User, student_id: int) -> StudentDashboardDetailsResponse:

        student = self._get_student(student_id)

        self._check_teacher_access(
            teacher=current_user,
            student_id=student.id,
        )

        student_words = self.student_word_repository.get_by_student(
            student.id,
        )

        return StudentDashboardDetailsResponse(
            student_id=student.id,
            name=student.name,
            email=student.email,
            words=[
                self._build_student_word_progress(item)
                for item in student_words
            ],
        )

    # Возвращает историю ответов ученика
    def get_student_history(self, current_user: User, student_id: int) -> StudentHistoryResponse:

        student = self._get_student(student_id)

        self._check_teacher_access(
            teacher=current_user,
            student_id=student.id,
        )

        history = self.exercise_result_repository.get_recent_answers_by_user(
            student.id,
        )

        return StudentHistoryResponse(
            student_id=student.id,
            student_name=student.name,
            history=[
                self._build_history_item(item)
                for item in history
            ],
        )

    # ==========================================================
    # Private methods
    # ==========================================================

    # Возвращает ученика или выбрасывает 404
    def _get_student(self, student_id: int) -> User:

        student = self.user_repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )

        return student

    # Проверяет, принадлежит ли ученик преподавателю
    def _check_teacher_access(self, teacher: User, student_id: int) -> None:

        if not self.teacher_student_repository.is_teacher_of_student(
            teacher.id,
            student_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student does not belong to this teacher",
            )

    # Формирует карточку ученика для списка Dashboard
    def _build_student_dashboard(self, student: User) -> StudentDashboardResponse:

        total_words = self.student_word_repository.count_by_student(student.id)

        due_words = self.student_word_repository.count_due_by_student(student.id)

        total_answers = self.exercise_result_repository.count_by_user(student.id)

        correct_answers = self.exercise_result_repository.count_correct_by_user(student.id)

        current_streak = self.student_word_repository.get_max_streak(student.id)

        return StudentDashboardResponse(
            student_id=student.id,
            name=student.name,
            email=student.email,
            total_words=total_words,
            due_words=due_words,
            total_answers=total_answers,
            correct_answers=correct_answers,
            accuracy=self._calculate_accuracy(
                total_answers,
                correct_answers,
            ),
            current_streak=current_streak,
        )

    # Рассчитывает процент правильных ответов
    def _calculate_accuracy(self, total_answers: int, correct_answers: int) -> float:

        if total_answers == 0:
            return 0

        return round(
            correct_answers / total_answers * 100,
            2,
        )

    # Формирует DTO прогресса одного слова
    def _build_student_word_progress(self, student_word: StudentWord,) -> StudentWordProgressResponse:

        return StudentWordProgressResponse(
            student_word_id=student_word.id,
            word_id=student_word.word.id,
            korean=student_word.word.korean,
            translation=student_word.word.translation,
            correct_streak=student_word.correct_streak,
            wrong_count=student_word.wrong_count,
            interval_days=student_word.interval_days,
            last_review_at=student_word.last_review_at,
            next_review_at=student_word.next_review_at,
        )

    # Формирует DTO одного ответа ученика
    def _build_history_item(self, exercise_result: ExerciseResult) -> ExerciseHistoryResponse:

        return ExerciseHistoryResponse(
            korean=exercise_result.word.korean,
            translation=exercise_result.word.translation,
            exercise_type=exercise_result.exercise_type,
            correct=exercise_result.correct,
            response=exercise_result.response,
            created_at=exercise_result.created_at,
        )