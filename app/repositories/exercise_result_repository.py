from sqlalchemy import select
from sqlalchemy.orm import Session

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

        return list(self.db.scalars(stmt))

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

        return list(self.db.scalars(stmt))

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

        return list(self.db.scalars(stmt))
