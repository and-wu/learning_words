from app.models.user import User
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.student_word_repository import StudentWordRepository
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.schemas.teacher_dashboard import StudentDashboardResponse


class TeacherDashboardService:

    def __init__(
        self,
        teacher_student_repository: TeacherStudentRepository,
        student_word_repository: StudentWordRepository,
        exercise_result_repository: ExerciseResultRepository,
    ):
        self.teacher_student_repository = teacher_student_repository
        self.student_word_repository = student_word_repository
        self.exercise_result_repository = exercise_result_repository

    # Возвращает список учеников преподавателя с краткой статистикой
    def get_students_dashboard(self, current_user: User) -> list[StudentDashboardResponse]:

        # Получаем всех учеников преподавателя
        students = self.teacher_student_repository.get_student_users(current_user.id)

        dashboard = []

        # Собираем статистику по каждому ученику
        for student in students:
            dashboard.append(
                self._build_student_dashboard(student)
            )

        return dashboard

    # Формирует статистику одного ученика
    def _build_student_dashboard(self, student: User) -> StudentDashboardResponse:

        # количество слов ученика
        total_words = self.student_word_repository.count_by_student(student_id=student.id)

        # количество слов к повторению
        due_words = self.student_word_repository.count_due_by_student(student_id=student.id)

        # всего ответов (выполненных упражнений)
        total_answers = self.exercise_result_repository.count_by_user(user_id=student.id)

        # количество правильных ответов
        correct_answers = self.exercise_result_repository.count_correct_by_user(user_id=student.id)

        # серия правильных ответов ученика
        current_streak = self.student_word_repository.get_max_streak(student_id=student.id)

        # процент правильных ответов ученика
        accuracy = self._calculate_accuracy(
            total_answers=total_answers,
            correct_answers=correct_answers,
        )

        return StudentDashboardResponse(
            student_id=student.id,
            name=student.name,
            email=student.email,
            total_words=total_words,
            due_words=due_words,
            total_answers=total_answers,
            correct_answers=correct_answers,
            accuracy=accuracy,
            current_streak=current_streak,
        )

    # Рассчитывает процент правильных ответов ученика
    def _calculate_accuracy(self, total_answers: int, correct_answers: int) -> float:

        if total_answers == 0:
            return 0

        return round(correct_answers / total_answers * 100, 2)


