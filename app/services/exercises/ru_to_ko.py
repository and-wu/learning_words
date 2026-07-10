from app.models.words import Word
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest

from .base import BaseExerciseHandler


class RuToKoExerciseHandler(BaseExerciseHandler):

    def build(self, word: Word) -> ExerciseContent:

        return ExerciseContent(
            question=word.translation,
        )


    def check(self, word: Word, data: SubmitExerciseRequest) -> bool:

        return (
            data.response.strip()
            ==
            word.korean.strip()
        )