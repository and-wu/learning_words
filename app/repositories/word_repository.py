from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Word


class WordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, word: Word) -> Word:
        self.db.add(word)
        self.db.flush()
        self.db.commit()
        self.db.refresh(word)

        return word

    def get_by_id(self, word_id: int) -> Word | None:
        stmt = (
            select(Word)
            .where(Word.id == word_id)
        )

        return self.db.scalar(stmt)

    def get_by_korean(self, korean: str) -> Word | None:
        stmt = (
            select(Word)
            .where(Word.korean == korean)
        )

        return self.db.scalar(stmt)

    def get_all(self) -> list[Word]:
        stmt = (
            select(Word)
            .order_by(Word.korean)
        )

        return self.db.scalars(stmt).all()

    # Получить случайные слова, кроме текущего
    def get_random_except(self, word_id: int, limit: int) -> list[Word]:
        stmt = (
            select(Word)
            .where(
                Word.id != word_id,
            )
            .order_by(
                func.random(),
            )
            .limit(limit)
        )

        return self.db.scalars(stmt).all()

    def update(self, word: Word) -> Word:

        self.db.flush()
        self.db.commit()
        self.db.refresh(word)

        return word

    def delete(self, word: Word) -> None:
        self.db.delete(word)
        self.db.commit()


