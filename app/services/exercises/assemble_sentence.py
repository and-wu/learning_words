from random import shuffle

from app.models import Word
from app.schemas.exercise_types import ExerciseContent
from app.schemas.exercises import SubmitExerciseRequest


class AssembleSentenceExerciseHandler:

    # Формирует упражнение
    def build(self, word: Word) -> ExerciseContent:

        ...

    # Проверяет ответ ученика
    def check(self, word: Word, data: SubmitExerciseRequest) -> bool:

        ...