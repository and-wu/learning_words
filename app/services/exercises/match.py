from random import shuffle

from app.models.words import Word
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest

from .base import BaseExerciseHandler
from ...repositories.word_repository import WordRepository


class MatchExerciseHandler(BaseExerciseHandler):

    def __init__(self, word_repository: WordRepository):
        self.word_repository = word_repository


    def build(self, word: Word) -> ExerciseContent:

        random_words = (
            self.word_repository.get_random_except(
                word_id=word.id,
                limit=3,
            )
        )

        options = [
            word.translation,
        ]

        options.extend(
            item.translation
            for item in random_words
        )

        shuffle(options)

        return ExerciseContent(
            question=word.korean,
            options=options,
        )


    def check(self, word: Word, data: SubmitExerciseRequest) -> bool:

        return (
            data.response.strip().lower()
            ==
            word.translation.strip().lower()
        )