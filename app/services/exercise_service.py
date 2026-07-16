from datetime import UTC, datetime, timedelta
from random import choice, shuffle

from fastapi import HTTPException, status

from app.enums.exercise_type import ExerciseType
from app.models import ExerciseResult, User, StudentWord, Word
from app.repositories.exercise_result_repository import ExerciseResultRepository
from app.repositories.student_word_repository import StudentWordRepository
from app.repositories.word_repository import WordRepository
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest
from app.schemas.next_exercise import NextExerciseResponse
from app.services.exercises.factory import ExerciseHandlerFactory

class ExerciseService:

    def __init__(
        self,
        exercise_result_repository: ExerciseResultRepository,
        student_word_repository: StudentWordRepository,
        word_repository: WordRepository,
        exercise_handler_factory: ExerciseHandlerFactory,
    ):
        self.exercise_result_repository = exercise_result_repository
        self.student_word_repository = student_word_repository
        self.word_repository = word_repository
        self.exercise_handler_factory = exercise_handler_factory

    # =====================================================
    # Public methods
    # =====================================================

    # Возвращает следующее упражнение для текущего ученика
    def get_next_exercise(self, current_user: User) -> NextExerciseResponse:

        student_word = self._get_random_due_word(current_user.id)

        exercise_type = self._choose_exercise_type()

        return self._build_exercise(
            student_word=student_word,
            exercise_type=exercise_type,
        )

    # Проверяет ответ ученика, сохраняет результат и обновляет прогресс
    def submit_answer(self, current_user: User, data: SubmitExerciseRequest) -> ExerciseResult:

        student_word = self._get_student_word(
            current_user=current_user,
            student_word_id=data.student_word_id,
        )

        word = self._get_word(student_word.word_id)

        correct = self._check_answer(
            word=word,
            data=data,
        )

        result = self._create_exercise_result(
            current_user=current_user,
            word=word,
            data=data,
            correct=correct,
        )

        self._update_student_progress(
            student_word=student_word,
            correct=correct,
        )

        return result

    # =====================================================
    # Exercise building
    # =====================================================

    # Возвращает случайное слово ученика, которое пора повторять
    def _get_random_due_word(self, student_id: int) -> StudentWord:

        due_words = self.student_word_repository.get_due_words(student_id)

        if not due_words:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No words available for review",
            )

        return choice(due_words)

    # Формирует готовое упражнение для выбранного слова
    def _build_exercise(self, student_word: StudentWord, exercise_type: ExerciseType) -> NextExerciseResponse:

        handler = self.exercise_handler_factory.get_handler(exercise_type)

        content = handler.build(student_word.word)

        return NextExerciseResponse(
            student_word_id=student_word.id,
            exercise_type=exercise_type,
            question=content.question,
            options=content.options,
        )

    # Проверяет правильность ответа ученика
    def _check_answer(self, word: Word, data: SubmitExerciseRequest,) -> bool:

        handler = self.exercise_handler_factory.get_handler(
            data.exercise_type,
        )

        return handler.check(
            word=word,
            data=data,
        )

    # =====================================================
    # Entity loading
    # =====================================================

    # Возвращает запись StudentWord и проверяет право доступа ученика
    def _get_student_word(self, current_user: User, student_word_id: int) -> StudentWord:

        student_word = self.student_word_repository.get_by_id(
            student_word_id,
        )

        if student_word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student word not found",
            )

        if student_word.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access this word",
            )

        return student_word

    # Возвращает слово из словаря или выбрасывает ошибку 404
    def _get_word(self, word_id: int) -> Word:

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        return word

    # =====================================================
    # Exercise results
    # =====================================================

    # Создает запись о выполненном упражнении
    def _create_exercise_result(
        self,
        current_user: User,
        word: Word,
        data: SubmitExerciseRequest,
        correct: bool,
    ) -> ExerciseResult:

        result = ExerciseResult(
            user_id=current_user.id,
            word_id=word.id,
            exercise_type=data.exercise_type,
            correct=correct,
            response=data.response,
        )

        return self.exercise_result_repository.create(result)

    # =====================================================
    # Progress
    # =====================================================

    # Обновляет статистику изучения слова после выполнения упражнения
    def _update_student_progress(self, student_word: StudentWord, correct: bool) -> None:

        if correct:
            self._apply_correct_answer(student_word)
        else:
            self._apply_wrong_answer(student_word)

        student_word.last_review_at = datetime.now(UTC)

        student_word.next_review_at = (
            student_word.last_review_at
            + timedelta(days=student_word.interval_days)
        )

        self.student_word_repository.update(student_word)

    # Обновляет прогресс после правильного ответа
    def _apply_correct_answer(
        self,
        student_word: StudentWord,
    ) -> None:

        student_word.correct_streak += 1

        student_word.interval_days = self._calculate_interval_days(
            student_word.correct_streak,
        )

    # Обновляет прогресс после неправильного ответа
    def _apply_wrong_answer(self, student_word: StudentWord) -> None:

        student_word.wrong_count += 1
        student_word.correct_streak = 0
        student_word.interval_days = 1

    # Рассчитывает следующий интервал повторения
    def _calculate_interval_days(self, streak: int) -> int:

        if streak <= 1:
            return 1

        if streak == 2:
            return 3

        if streak == 3:
            return 7

        return 14

    # =====================================================
    # Helpers
    # =====================================================

    # Выбирает случайный тип упражнения
    def _choose_exercise_type(self) -> ExerciseType:

        return choice(
            (
                ExerciseType.KO_TO_RU,
                ExerciseType.RU_TO_KO,
                ExerciseType.MATCH,
            )
        )