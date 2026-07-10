from app.models.exercise_result import ExerciseType

from app.services.exercises.base import BaseExerciseHandler
from app.services.exercises.ko_to_ru import KoToRuExerciseHandler
from app.services.exercises.ru_to_ko import RuToKoExerciseHandler
from app.services.exercises.match import MatchExerciseHandler


class ExerciseHandlerFactory:
    """
    Создает нужный обработчик упражнения
    в зависимости от его типа.
    """

    def __init__(self, word_repository):
        self.word_repository = word_repository


    # Возвращает обработчик для конкретного типа упражнения
    def get_handler(self, exercise_type: ExerciseType) -> BaseExerciseHandler:

        # Упражнение: корейский -> русский
        if exercise_type == ExerciseType.KO_TO_RU:
            return KoToRuExerciseHandler()


        # Упражнение: русский -> корейский
        if exercise_type == ExerciseType.RU_TO_KO:
            return RuToKoExerciseHandler()


        # Упражнение: выбрать правильный перевод
        if exercise_type == ExerciseType.MATCH:
            return MatchExerciseHandler(
                word_repository=self.word_repository,
            )


        raise ValueError(
            f"Unsupported exercise type: {exercise_type}"
        )