from abc import ABC, abstractmethod

from app.models.words import Word
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest
from app.models.exercise_result import ExerciseType


class BaseExerciseHandler(ABC):

    @abstractmethod
    def build(self, word: Word) -> ExerciseContent:
        pass


    @abstractmethod
    def check(self, word: Word, data: SubmitExerciseRequest) -> bool:
        pass