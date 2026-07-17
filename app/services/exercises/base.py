from abc import ABC, abstractmethod

from app.models.words import Word
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest


class BaseExerciseHandler(ABC):
    """Базовый интерфейс всех упражнений."""

    @abstractmethod
    def build(self, word: Word) -> ExerciseContent:
        """Формирует данные для отображения упражнения."""
        pass


    @abstractmethod
    def check(self, word: Word, data: SubmitExerciseRequest) -> bool:
        """Проверяет правильность ответа ученика."""
        pass