from app.models.exercise_result import ExerciseType
from app.repositories.word_repository import WordRepository

from app.services.exercises.base import BaseExerciseHandler
from app.services.exercises.ko_to_ru import KoToRuExerciseHandler
from app.services.exercises.ru_to_ko import RuToKoExerciseHandler
from app.services.exercises.match import MatchExerciseHandler


class ExerciseHandlerFactory:
    """
    Создает нужный обработчик упражнения
    в зависимости от его типа.
    """

    def __init__(self, word_repository: WordRepository):
        self.word_repository = word_repository


    # Возвращает обработчик для конкретного типа упражнения
    def get_handler(self, exercise_type: ExerciseType) -> BaseExerciseHandler:

        handlers = {
            ExerciseType.KO_TO_RU: lambda: KoToRuExerciseHandler(),
            ExerciseType.RU_TO_KO: lambda: RuToKoExerciseHandler(),
            ExerciseType.MATCH: lambda: MatchExerciseHandler(
                word_repository=self.word_repository,
            ),
        }

        factory = handlers[exercise_type]

        if factory is None:
            raise ValueError(
                f"Unsupported exercise type: {exercise_type}"
            )

        return factory()
