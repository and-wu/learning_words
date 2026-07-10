from datetime import datetime, UTC

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

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

    # Получить все слова, которые пора повторять
    def get_due_words(self, student_id: int) -> list[StudentWord]:
        stmt = (
            select(StudentWord)
            .options(
                selectinload(StudentWord.word),
            )
            .where(
                StudentWord.student_id == student_id,
                StudentWord.next_review_at <= datetime.now(UTC),
            )
        )

        return list(self.db.scalars(stmt).all())

    # Возвращает количество слов, назначенных ученику
    def count_by_student(self, student_id: int) -> int:
        stmt = (
            select(func.count(StudentWord.id))
            .where(
                StudentWord.student_id == student_id,
            )
        )

        return self.db.scalar(stmt) or 0

    # Возвращает количество слов, которые нужно повторить
    def count_due_by_student(self, student_id: int) -> int:
        stmt = (
            select(func.count(StudentWord.id))
            .where(
                StudentWord.student_id == student_id,
                StudentWord.next_review_at <= datetime.now(UTC),
            )
        )

        return self.db.scalar(stmt) or 0

    # Возвращает максимальную серию правильных ответов ученика
    def get_max_streak(self, student_id: int ) -> int:
        stmt = (
            select(func.max(StudentWord.correct_streak))
            .where(
                StudentWord.student_id == student_id,
            )
        )

        return self.db.scalar(stmt) or 0