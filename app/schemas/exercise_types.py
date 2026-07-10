from dataclasses import dataclass


@dataclass
class ExerciseContent:
    """Данные, необходимые для отображения упражнения."""
    question: str
    options: list[str] | None = None