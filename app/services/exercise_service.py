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



    def get_next_exercise(self, current_user: User) -> NextExerciseResponse:

        # Получаем все слова, которые пора повторить
        due_words = self.student_word_repository.get_due_words(current_user.id)

        # Если повторять нечего
        if not due_words:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No words available for review",
            )

        # Выбираем случайное слово
        student_word = choice(due_words)

        # Выбираем тип упражнения
        exercise_type = self._choose_exercise_type()

        # Получаем обработчик конкретного упражнения
        handler = self.exercise_handler_factory.get_handler(exercise_type)

        # Формируем содержимое упражнения
        content = handler.build(
            student_word.word,
        )


        # Возвращаем упражнение
        return NextExerciseResponse(
            student_word_id=student_word.id,
            exercise_type=exercise_type,
            question=content.question,
            options=content.options,
        )

    def submit_answer(self, current_user: User, data: SubmitExerciseRequest) -> ExerciseResult:

        # Получаем слово ученика по идентификатору
        student_word = self._get_student_word(
            current_user=current_user,
            student_word_id=data.student_word_id,
        )

        # Получаем слово из словаря ученика
        word = self._get_word(student_word.word_id)

        # Получаем обработчик упражнения
        handler = self.exercise_handler_factory.get_handler(
            data.exercise_type,
        )

        # Проверяем правильность ответа ученика
        correct = handler.check(word=word, data=data,)

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

    # Получаем слово из словаря ученика
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

    # # Проверяет правильность ответа ученика
    # def _check_answer(self, word: Word, data: SubmitExerciseRequest) -> bool:
    #
    #     # Подготавливаем ответ ученика
    #     response = data.response.strip()
    #
    #     # Проверяем упражнения, где ответом является русский перевод
    #     if data.exercise_type in (
    #             ExerciseType.KO_TO_RU,
    #             ExerciseType.MATCH,
    #     ):
    #         return (
    #                 response.lower()
    #                 ==
    #                 word.translation.strip().lower()
    #         )
    #
    #     # Проверяем упражнение "Русский → Корейский"
    #     if data.exercise_type == ExerciseType.RU_TO_KO:
    #         return (
    #                 response
    #                 ==
    #                 word.korean.strip()
    #         )
    #
    #     # Остальные упражнения пока не реализованы
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Exercise type '{data.exercise_type.value}' is not supported yet",
    #     )

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

    def _choose_exercise_type(self) -> ExerciseType:

        return choice(
            [
                ExerciseType.KO_TO_RU,
                ExerciseType.RU_TO_KO,
                ExerciseType.MATCH
            ]
        )

    # # Сформировать вопрос для упражнения
    # def _build_question(self, word: Word, exercise_type: ExerciseType) -> ExerciseContent:
    #
    #     # Корейское слово → нужно выбрать русский перевод
    #     if exercise_type == ExerciseType.KO_TO_RU:
    #         return ExerciseContent(
    #             question=word.korean,
    #         )
    #
    #     # Русский перевод → нужно написать корейское слово
    #     if exercise_type == ExerciseType.RU_TO_KO:
    #         return ExerciseContent(
    #             question=word.translation,
    #         )
    #
    #     # Выбрать правильный перевод из нескольких вариантов
    #     if exercise_type == ExerciseType.MATCH:
    #         return ExerciseContent(
    #             question=word.korean,
    #             options=self._build_options(word),
    #         )
    #
    #     raise ValueError(
    #             f"Unsupported exercise type: {exercise_type}"
    #         )
    #
    # # Сформировать варианты ответа для упражнения Match
    # def _build_options(self, word: Word) -> list[str]:
    #
    #     # Получаем три случайных неправильных слова
    #     random_words = self.word_repository.get_random_except(
    #         word_id=word.id,
    #         limit=3,
    #     )
    #
    #     # Добавляем правильный ответ
    #     options = [word.translation]
    #
    #     # Добавляем неправильные варианты
    #     options.extend(
    #         random_word.translation
    #         for random_word in random_words
    #     )
    #
    #     # Перемешиваем варианты
    #     shuffle(options)
    #
    #     return options