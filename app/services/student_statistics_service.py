from app.models.user import User
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.student_word_repository import StudentWordRepository
from app.schemas.statistics import StudentStatisticsResponse


class StudentStatisticsService:

    def __init__(
        self,
        student_word_repository: StudentWordRepository,
        exercise_result_repository: ExerciseResultRepository,
    ):
        self.student_word_repository = student_word_repository
        self.exercise_result_repository = exercise_result_repository

    # Возвращает статистику ученика
    def get_statistics(self, current_user: User) -> StudentStatisticsResponse:

        # Получаем количество назначенных слов
        total_words = self.student_word_repository.count_by_student(
            current_user.id,
        )

        # Получаем количество слов, которые нужно повторить
        due_words = self.student_word_repository.count_due_by_student(
            current_user.id,
        )

        # Получаем количество выполненных упражнений
        total_answers = self.exercise_result_repository.count_by_user(
            current_user.id,
        )

        # Получаем количество правильных ответов
        correct_answers = self.exercise_result_repository.count_correct_by_user(
            current_user.id,
        )

        # Получаем количество неправильных ответов
        wrong_answers = self.exercise_result_repository.count_wrong_by_user(
            current_user.id,
        )

        # Получаем максимальную серию правильных ответов
        current_streak = self.student_word_repository.get_max_streak(
            current_user.id,
        )

        # Рассчитываем процент правильных ответов
        if total_answers == 0:
            accuracy = 0
        else:
            accuracy = round(
                correct_answers / total_answers * 100,
                2,
            )

        return StudentStatisticsResponse(
            total_words=total_words,
            due_words=due_words,
            total_answers=total_answers,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
            accuracy=accuracy,
            current_streak=current_streak,
        )

