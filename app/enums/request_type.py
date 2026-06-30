from enum import Enum


class RequestType(str, Enum):
    TEACHER_TO_STUDENT = "teacher_to_student"
    STUDENT_TO_TEACHER = "student_to_teacher"