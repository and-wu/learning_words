from fastapi import HTTPException, status

from app.enums.source_type import SourceType
from app.enums.user_role import UserRole
from app.models import StudentWord, User, Word
from app.repositories.student_word_repository import StudentWordRepository
from app.repositories.teacher_student_repository import TeacherStudentRepository
from app.repositories.user_repository import UserRepository
from app.repositories.word_repository import WordRepository


class StudentWordService:

    def __init__(
        self,
        user_repository: UserRepository,
        word_repository: WordRepository,
        teacher_student_repository: TeacherStudentRepository,
        student_word_repository: StudentWordRepository,
    ):
        self.user_repository = user_repository
        self.word_repository = word_repository
        self.teacher_student_repository = teacher_student_repository
        self.student_word_repository = student_word_repository

    # ==========================================================
    # Public methods
    # ==========================================================

    # Назначает слово ученику преподавателем
    def assign_by_teacher(self, teacher: User, student_id: int, word_id: int) -> StudentWord:

        self._ensure_teacher(teacher)

        student = self._get_student(student_id)

        self._ensure_teacher_student_relation(
            teacher.id,
            student.id,
        )

        word = self._get_word(word_id)

        self._ensure_word_not_assigned(
            student.id,
            word.id,
        )

        return self._create_student_word(
            student_id=student.id,
            word_id=word.id,
            assigned_by=teacher.id,
            source_type=SourceType.TEACHER,
        )

    # Добавляет слово самому себе
    def assign_to_self(self, student: User, word_id: int) -> StudentWord:

        self._ensure_student(student)

        word = self._get_word(word_id)

        self._ensure_word_not_assigned(
            student.id,
            word.id,
        )

        return self._create_student_word(
            student_id=student.id,
            word_id=word.id,
            assigned_by=student.id,
            source_type=SourceType.SELF,
        )

    # Возвращает список слов текущего ученика
    def get_student_words(self, current_user: User) -> list[StudentWord]:

        self._ensure_student(current_user)

        return self.student_word_repository.get_by_student(
            current_user.id,
        )

    # Удаляет слово из словаря ученика
    def remove(self, current_user: User, student_word_id: int) -> None:

        student_word = self._get_student_word(student_word_id)

        self._ensure_can_remove(
            current_user,
            student_word,
        )

        self.student_word_repository.delete(student_word)

    # ==========================================================
    # Private methods
    # ==========================================================

    # Проверяет, что пользователь является преподавателем
    def _ensure_teacher(self, user: User) -> None:

        if user.role != UserRole.TEACHER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only teachers can assign words",
            )

    # Проверяет, что пользователь является учеником
    def _ensure_student(self, user: User) -> None:

        if user.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only students can perform this action",
            )

    # Возвращает ученика по id
    def _get_student(self, student_id: int) -> User:

        student = self.user_repository.get_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found",
            )

        if student.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a student",
            )

        return student

    # Возвращает слово по id
    def _get_word(self, word_id: int) -> Word:

        word = self.word_repository.get_by_id(word_id)

        if word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Word not found",
            )

        return word

    # Проверяет существование связи преподавателя и ученика
    def _ensure_teacher_student_relation(self, teacher_id: int, student_id: int) -> None:

        if not self.teacher_student_repository.is_teacher_of_student(
            teacher_id,
            student_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teacher and student are not connected",
            )

    # Проверяет, что слово еще не назначено ученику
    def _ensure_word_not_assigned(self, student_id: int, word_id: int) -> None:

        if self.student_word_repository.exists(
            student_id,
            word_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Word already assigned",
            )

    # Создает запись StudentWord
    def _create_student_word(
        self,
        student_id: int,
        word_id: int,
        assigned_by: int,
        source_type: SourceType,
    ) -> StudentWord:

        student_word = StudentWord(
            student_id=student_id,
            word_id=word_id,
            assigned_by=assigned_by,
            source_type=source_type,
        )

        return self.student_word_repository.create(student_word)

    # Возвращает StudentWord по id
    def _get_student_word(self, student_word_id: int) -> StudentWord:

        student_word = self.student_word_repository.get_by_id(student_word_id)

        if student_word is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student word not found",
            )

        return student_word

    # Проверяет право пользователя удалить слово
    def _ensure_can_remove(self, current_user: User, student_word: StudentWord) -> None:

        if (
            current_user.id != student_word.student_id
            and current_user.id != student_word.assigned_by
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot remove this word",
            )

        if (
            current_user.role == UserRole.TEACHER
            and student_word.source_type != SourceType.TEACHER
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teacher cannot remove student's own word",
            )