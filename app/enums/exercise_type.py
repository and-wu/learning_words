from enum import Enum


class ExerciseType(str, Enum):
    MATCH = "match"
    KO_TO_RU = "ko_to_ru"
    RU_TO_KO = "ru_to_ko"
    ASSEMBLE_SENTENCE = "assemble_sentence"