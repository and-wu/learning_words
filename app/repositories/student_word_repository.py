from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student_words import StudentWord


class StudentWordRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, student_word: StudentWord) -> StudentWord:
        self.db.add(student_word)
        self.db.commit()
        self.db.refresh(student_word)

        return student_word

    def get_by_id(self, student_word_id: int) -> StudentWord | None:
        stmt = (
            select(StudentWord)
            .where(
                StudentWord.id == student_word_id,
            )
        )

        return self.db.scalar(stmt)

    def get_student_words(self, student_id: int) -> list[StudentWord]:
        stmt = (
            select(StudentWord)
            .where(
                StudentWord.student_id == student_id,
            )
        )

        return list(self.db.scalars(stmt))

    def exists(self, student_id: int, word_id: int) -> bool:
        stmt = (
            select(StudentWord)
            .where(
                StudentWord.student_id == student_id,
                StudentWord.word_id == word_id,
            )
        )

        return self.db.scalar(stmt) is not None

    def update(self, student_word: StudentWord) -> StudentWord:
        self.db.add(student_word)
        self.db.commit()
        self.db.refresh(student_word)

        return student_word

    def delete(self, student_word: StudentWord) -> None:
        self.db.delete(student_word)
        self.db.commit()