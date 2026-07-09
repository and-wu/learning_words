from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status

from app.enums.exercise_type import ExerciseType
from app.models import ExerciseResult, User, StudentWord, Word
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.student_words_repository import StudentWordRepository
from app.repositories.word_repository import WordRepository
from app.schemas.exercises import SubmitExerciseRequest


class ExerciseService:

    def __init__(
        self,
        exercise_result_repository: ExerciseResultRepository,
        student_word_repository: StudentWordRepository,
        word_repository: WordRepository,
    ):
        self.exercise_result_repository = exercise_result_repository
        self.student_word_repository = student_word_repository
        self.word_repository = word_repository

    def submit_answer(self, current_user: User, data: SubmitExerciseRequest) -> ExerciseResult:

        # Получаем слово ученика по идентификатору
        student_word = self._get_student_word(
            current_user=current_user,
            student_word_id=data.student_word_id,
        )

        # Получаем слово из словаря
        word = self._get_word(student_word.word_id)

        # Проверяем правильность ответа ученика
        correct = self._check_answer(word=word, data=data)

        # Сохраняем результат упражнения в историю
        exercise_result = self._create_exercise_result(
            current_user=current_user,
            word=word,
            data=data,
            correct=correct,
        )

        # Обновляем прогресс после правильного ответа
        self._update_student_progress(student_word=student_word, correct=correct)

        return exercise_result

    # Получает слово ученика и проверяет право доступа
    def _get_student_word(self, current_user: User, student_word_id: int) -> StudentWord:

        # Получаем слово ученика по идентификатору
        student_word = self.student_word_repository.get_by_id(student_word_id)

        # Проверяем, что слово существует
        if student_word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student word not found",
            )

        # Проверяем, что слово принадлежит текущему ученику
        if student_word.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access this word",
            )

        return student_word

    def _get_word(self, word_id: int) -> Word:
        # Получаем слово, связанное с записью ученика
        word = self.word_repository.get_by_id(word_id)

        # Проверяем, что слово существует
        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        return word

    # Проверяет правильность ответа ученика
    def _check_answer(
            self,
            word: Word,
            data: SubmitExerciseRequest,
    ) -> bool:

        # Проверяем упражнение "Корейский → Русский"
        if data.exercise_type == ExerciseType.KO_TO_RU:
            return (
                    data.response.strip().lower()
                    ==
                    word.translation.strip().lower()
            )

        # Проверяем упражнение "Русский → Корейский"
        if data.exercise_type == ExerciseType.RU_TO_KO:
            return (
                    data.response.strip()
                    ==
                    word.korean.strip()
            )

        # Остальные упражнения пока не реализованы
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise type is not supported yet",
        )

    # Создает запись о результате выполнения упражнения
    def _create_exercise_result(
            self,
            current_user: User,
            word: Word,
            data: SubmitExerciseRequest,
            correct: bool,
    ) -> ExerciseResult:

        exercise_result = ExerciseResult(
            user_id=current_user.id,
            word_id=word.id,
            exercise_type=data.exercise_type,
            correct=correct,
            response=data.response,
        )

        return self.exercise_result_repository.create(
            exercise_result,
        )

    # функция обновления прогресса
    def _update_student_progress(self, student_word: StudentWord, correct: bool) -> None:

        # Обновляем статистику в зависимости от результата ответа
        if correct:

            student_word.correct_streak += 1

            student_word.interval_days = (
                self._calculate_interval_days(
                    student_word.correct_streak,
                )
            )

        else:

            student_word.wrong_count += 1

            student_word.correct_streak = 0

            student_word.interval_days = 1

        # Сохраняем время последнего повторения
        student_word.last_review_at = datetime.now(UTC)

        # Рассчитываем дату следующего повторения
        student_word.next_review_at = (
                student_word.last_review_at
                + timedelta(days=student_word.interval_days)
        )

        # Записываем изменения в базу данных
        self.student_word_repository.update(student_word)

    # функция вычисления интервала
    def _calculate_interval_days(self, correct_streak: int) -> int:

        if correct_streak <= 1:
            return 1

        if correct_streak == 2:
            return 3

        if correct_streak == 3:
            return 7

        return 14