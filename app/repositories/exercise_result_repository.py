from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.models import ExerciseResult


class ExerciseResultRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, result: ExerciseResult) -> ExerciseResult:
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def get_by_id(self, result_id: int) -> ExerciseResult | None:
        stmt = (
            select(ExerciseResult)
            .where(
                ExerciseResult.id == result_id,
            )
        )

        return self.db.scalar(stmt)

    def get_by_user(self, user_id: int) -> list[ExerciseResult]:
        stmt = (
            select(ExerciseResult)
            .where(
                ExerciseResult.user_id == user_id,
            )
            .order_by(
                ExerciseResult.created_at.desc(),
            )
        )

        return self.db.scalars(stmt).all()

    def get_by_word(self, word_id: int) -> list[ExerciseResult]:
        stmt = (
            select(ExerciseResult)
            .where(
                ExerciseResult.word_id == word_id,
            )
            .order_by(
                ExerciseResult.created_at.desc(),
            )
        )

        return self.db.scalars(stmt).all()

    def get_by_user_and_word(self, user_id: int, word_id: int) -> list[ExerciseResult]:
        stmt = (
            select(ExerciseResult)
            .where(
                ExerciseResult.user_id == user_id,
                ExerciseResult.word_id == word_id,
            )
            .order_by(
                ExerciseResult.created_at.desc(),
            )
        )

        return self.db.scalars(stmt).all()

    # Возвращает общее количество выполненных упражнений ученика
    def count_by_user(self, user_id: int) -> int:
        stmt = (
            select(func.count(ExerciseResult.id))
            .where(
                ExerciseResult.user_id == user_id,
            )
        )

        return self.db.scalar(stmt) or 0

    # Возвращает количество правильных ответов ученика
    def count_correct_by_user(self, user_id: int) -> int:
        stmt = (
            select(func.count(ExerciseResult.id))
            .where(
                ExerciseResult.user_id == user_id,
                ExerciseResult.correct.is_(True),
            )
        )

        return self.db.scalar(stmt) or 0

    # Возвращает количество неправильных ответов ученика
    def count_wrong_by_user(self, user_id: int) -> int:
        stmt = (
            select(func.count(ExerciseResult.id))
            .where(
                ExerciseResult.user_id == user_id,
                ExerciseResult.correct.is_(False),
            )
        )

        return self.db.scalar(stmt) or 0

    # Возвращает последние ответы ученика
    def get_recent_answers_by_user(self, user_id: int, limit: int = 50) -> list[ExerciseResult]:

        stmt = (
            select(ExerciseResult)
            .options(
                joinedload(ExerciseResult.word),
            )
            .where(
                ExerciseResult.user_id == user_id,
            )
            .order_by(
                ExerciseResult.created_at.desc(),
                ExerciseResult.id.desc(),
            )
            .limit(limit)
        )

        return self.db.scalars(stmt).all()

    
