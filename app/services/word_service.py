from fastapi import HTTPException, status

from app.models import Word
from app.repositories.word_repository import WordRepository
from app.schemas.words import CreateWordRequest, UpdateWordRequest


class WordService:
    def __init__(self, word_repository: WordRepository):
        self.word_repository = word_repository

    def create(self, data: CreateWordRequest, created_by: int) -> Word:

        existing_word = self.word_repository.get_by_korean(data.korean)

        if existing_word is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Word already exists",
            )

        word = Word(
            korean=data.korean,
            translation=data.translation,
            part_of_speech=data.part_of_speech,
            comment=data.comment,
            created_by=created_by,
        )

        return self.word_repository.create(word)

    def get_all(self) -> list[Word]:
        return self.word_repository.get_all()

    def get_by_id(self, word_id: int) -> Word:

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        return word

    def update(self, word_id: int, data: UpdateWordRequest) -> Word:

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        if data.korean is not None and data.korean != word.korean:

            existing_word = self.word_repository.get_by_korean(data.korean)

            if existing_word is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Word already exists",
                )

            word.korean = data.korean

        if data.translation is not None:
            word.translation = data.translation

        if data.part_of_speech is not None:
            word.part_of_speech = data.part_of_speech

        if data.comment is not None:
            word.comment = data.comment

        return self.word_repository.update(word)

    def delete(self, word_id: int) -> None:

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        self.word_repository.delete(word)