from enum import Enum


class UserRole(str, Enum):
    teacher = "teacher"
    student = "student"