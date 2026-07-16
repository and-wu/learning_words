from fastapi import HTTPException, status

from app.models import Word
from app.repositories.word_repository import WordRepository
from app.schemas.words import CreateWordRequest, UpdateWordRequest


class WordService:
    def __init__(self, word_repository: WordRepository):
        self.word_repository = word_repository

    # ==========================================
    # Public methods
    # ==========================================

    def create(self, data: CreateWordRequest, created_by: int) -> Word:

        self._validate_korean_unique(data.korean)

        return self._create_word(
            data=data,
            created_by=created_by,
        )

    # Возвращает все слова
    def get_all(self) -> list[Word]:
        return self.word_repository.get_all()

    # Возвращает слово по id
    def get_by_id(self, word_id: int) -> Word:
        return self._get_word(word_id)

    # Обновляет существующее слово
    def update(self, word_id: int, data: UpdateWordRequest) -> Word:

        word = self._get_word(word_id)

        if data.korean is not None and data.korean != word.korean:
            self._validate_korean_unique(data.korean)
            word.korean = data.korean

        self._update_word_fields(
            word=word,
            data=data,
        )

        return self.word_repository.update(word)

    # Удаляет слово
    def delete(self, word_id: int) -> None:

        word = self._get_word(word_id)

        self.word_repository.delete(word)


    # ==========================================
    # Private methods
    # ==========================================

    # Возвращает слово или выбрасывает 404
    def _get_word(self, word_id: int) -> Word:
        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        return word

    # Проверяет уникальность корейского слова
    def _validate_korean_unique(self, korean: str) -> None:

        existing_word = self.word_repository.get_by_korean(korean)

        if existing_word is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Word already exists",
            )

    # Создает объект Word и сохраняет его
    def _create_word(self, data: CreateWordRequest, created_by: int) -> Word:

        word = Word(
            korean=data.korean,
            translation=data.translation,
            part_of_speech=data.part_of_speech,
            comment=data.comment,
            created_by=created_by,
        )

        return self.word_repository.create(word)

    # Обновляет поля существующего слова
    def _update_word_fields(self, word: Word, data: UpdateWordRequest) -> None:

        if data.translation is not None:
            word.translation = data.translation

        if data.part_of_speech is not None:
            word.part_of_speech = data.part_of_speech

        if data.comment is not None:
            word.comment = data.comment