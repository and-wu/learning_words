from app.models.words import Word
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest
from app.models.exercise_result import ExerciseType

from .base import BaseExerciseHandler


class KoToRuExerciseHandler(BaseExerciseHandler):

    def build(self, word: Word) -> ExerciseContent:

        return ExerciseContent(
            question=word.korean,
        )


    def check(self, word: Word,data: SubmitExerciseRequest) -> bool:

        return (
            data.response.strip().lower()
            ==
            word.translation.strip().lower()
        )