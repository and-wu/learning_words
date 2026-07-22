# Learning Words API

Backend API for a Korean vocabulary learning platform with teacher–student collaboration, spaced repetition, interactive exercises, and learning progress tracking.

---

## About

**Learning Words API** is a REST backend for a Korean vocabulary learning platform.

The application allows users to:

* register and authenticate using session cookies;
* work with Korean vocabulary;
* create teacher–student relationships;
* assign vocabulary to students;
* study words using spaced repetition;
* complete interactive exercises;
* track learning progress and statistics;
* monitor student performance through a teacher dashboard.

The project is built with a layered architecture that separates HTTP handling, business logic, data access, and database models.

---

## Architecture

The project follows a layered architecture:

```text
HTTP Request
     │
     ▼
  Routers
     │
     ▼
  Services
     │
     ▼
Repositories
     │
     ▼
 SQLAlchemy ORM
     │
     ▼
 PostgreSQL
```

### Main layers

#### Routers

Responsible for:

* HTTP endpoints;
* request validation;
* dependency injection;
* response models.

#### Services

Contain business logic:

* authentication;
* teacher–student relationships;
* vocabulary management;
* student vocabulary;
* exercises;
* spaced repetition;
* statistics;
* teacher dashboard.

#### Repositories

Responsible for database access:

* querying data;
* creating records;
* updating records;
* deleting records;
* aggregate queries.

#### Models

SQLAlchemy ORM models representing database entities.

#### Schemas

Pydantic models used for:

* request validation;
* response serialization;
* API contracts.

---

## Features

### Authentication

Implemented:

* user registration;
* login;
* logout;
* cookie-based session authentication;
* current user endpoint;
* password hashing;
* session expiration;
* role-based user types.

Supported roles:

* `teacher`;
* `student`.

Authentication uses a secure HTTP-only cookie containing the session token.

---

### Teacher–Student Relationships

Implemented:

* teacher-to-student connection requests;
* student-to-teacher connection requests;
* incoming requests;
* outgoing requests;
* accepting requests;
* rejecting requests;
* viewing students;
* viewing teachers;
* deactivating relationships.

Request statuses:

```text
pending
accepted
rejected
cancelled
```

---

### Vocabulary

Implemented:

* create words;
* retrieve all words;
* retrieve a word by ID;
* update words;
* delete words;
* duplicate Korean word validation.

A word contains:

* Korean text;
* translation;
* part of speech;
* comment;
* author.

---

### Student Vocabulary

Implemented:

* teacher assignment of words to students;
* students adding words to their own vocabulary;
* duplicate assignment protection;
* teacher–student access validation;
* removing assigned words;
* tracking learning progress.

Each student word tracks:

* correct answer streak;
* wrong answer count;
* current interval;
* last review date;
* next review date;
* assignment source.

Possible sources:

```text
teacher
self
```

---

### Spaced Repetition

The current learning interval is calculated based on the correct answer streak.

Current schedule:

| Correct streak | Interval |
| -------------- | -------: |
| 0              |    1 day |
| 1              |    1 day |
| 2              |   3 days |
| 3              |   7 days |
| 4+             |  14 days |

When a student answers incorrectly:

* the correct streak is reset;
* the wrong answer counter is increased;
* the interval is reset to 1 day.

When a student answers correctly:

* the correct streak is increased;
* the next interval is calculated;
* the next review date is scheduled.

---

### Exercises

Implemented exercise types:

* Korean → Russian;
* Russian → Korean;
* Matching.

Exercise handlers are separated using a handler-based architecture:

```text
ExerciseService
      │
      ▼
ExerciseHandlerFactory
      │
      ├── KoToRuExerciseHandler
      ├── RuToKoExerciseHandler
      └── MatchExerciseHandler
```

Each exercise handler is responsible for:

* building exercise content;
* checking the student's answer.

Supported exercise types:

```text
ko_to_ru
ru_to_ko
match
assemble_sentence
```

`assemble_sentence` is currently reserved for future implementation.

---

### Learning Statistics

Implemented:

* total assigned words;
* words currently due for review;
* total exercise answers;
* correct answers;
* incorrect answers;
* accuracy percentage;
* maximum correct answer streak.

---

### Teacher Dashboard

Implemented:

* list of connected students;
* summary statistics for each student;
* detailed student vocabulary progress;
* exercise history;
* student accuracy;
* review statistics.

Teachers can view:

* total vocabulary size;
* words due for review;
* number of completed exercises;
* number of correct answers;
* accuracy percentage;
* maximum correct streak;
* progress for individual words;
* recent exercise history.

---

## API Modules

Current API modules:

```text
/auth
/words
/student_word
/teacher_students
/teacher-student-requests
/statistics
/teacher/dashboard
```

Interactive API documentation is available through Swagger UI.

---

## Technology Stack

* Python 3.13
* FastAPI
* SQLAlchemy 2.0
* PostgreSQL
* Alembic
* Pydantic v2
* pydantic-settings
* bcrypt
* Uvicorn

---

## Project Structure

```text
.
├── app/
│   ├── config/
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── services.py
│   │
│   ├── enums/
│   │   ├── exercise_type.py
│   │   ├── request_status.py
│   │   ├── request_type.py
│   │   ├── source_type.py
│   │   └── user_role.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── word.py
│   │   ├── student_word.py
│   │   ├── exercise_result.py
│   │   ├── teacher_student.py
│   │   ├── teacher_student_request.py
│   │   └── ...
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── session_repository.py
│   │   ├── word_repository.py
│   │   ├── student_word_repository.py
│   │   ├── exercise_result_repository.py
│   │   ├── teacher_student_repository.py
│   │   └── ...
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── word.py
│   │   ├── student_word.py
│   │   ├── exercise.py
│   │   ├── statistics.py
│   │   ├── teacher_student.py
│   │   ├── teacher_student_request.py
│   │   └── teacher_dashboard.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── words.py
│   │   ├── student_words.py
│   │   ├── exercises.py
│   │   ├── statistics.py
│   │   └── teacher_dashboard.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── current_user_service.py
│   │   ├── word_service.py
│   │   ├── student_word_service.py
│   │   ├── exercise_service.py
│   │   ├── student_statistics_service.py
│   │   ├── teacher_student_service.py
│   │   ├── teacher_student_request_service.py
│   │   ├── teacher_dashboard_service.py
│   │   │
│   │   └── exercises/
│   │       ├── base.py
│   │       ├── factory.py
│   │       ├── ko_to_ru.py
│   │       ├── ru_to_ko.py
│   │       └── match.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .env
├── alembic.ini
├── pyproject.toml
└── README.md
```

---

## Database

The project uses PostgreSQL and SQLAlchemy ORM.

The database schema is managed through Alembic migrations.

Current domain entities include:

```text
User
Session
Word
StudentWord
ExerciseResult
TeacherStudent
TeacherStudentRequest
```

The database contains relationships between:

```text
User
  │
  ├── Sessions
  ├── Words
  ├── StudentWords
  ├── ExerciseResults
  ├── Teacher–Student Relationships
  └── Teacher–Student Requests
```

---

## Configuration

Application configuration is loaded from environment variables.

Example:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/learning_words
```

The application uses `pydantic-settings` to load configuration from `.env`.

---

## Installation

Install project dependencies:

```bash
uv sync
```

Make sure PostgreSQL is running and configure the database connection in `.env`.

---

## Database Migrations

Apply all migrations:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe your changes"
```

Apply the latest migration:

```bash
alembic upgrade head
```

---

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Development Status

### Completed

* layered backend architecture;
* authentication;
* password hashing;
* cookie-based sessions;
* current user dependency;
* teacher–student requests;
* teacher–student relationships;
* vocabulary management;
* student vocabulary;
* spaced repetition logic;
* exercise handlers;
* exercise factory;
* exercise result history;
* student statistics;
* teacher dashboard;
* Alembic integration;
* environment-based configuration.

### Next Development Steps

1. Add automated tests.
2. Improve validation and error handling.
3. Add pagination for large collections.
4. Optimize database queries.
5. Add API integration tests.
6. Improve exercise architecture.
7. Implement sentence assembly exercises.
8. Add Flutter mobile client.
9. Add production configuration.
10. Add Docker deployment.

---

## Testing

Automated tests are planned as the next major development stage.

The planned test structure:

```text
tests/
├── unit/
│   ├── services/
│   └── exercise_handlers/
│
└── integration/
    ├── auth/
    ├── words/
    ├── exercises/
    └── teacher_dashboard/
```

Important areas for testing:

* authentication;
* session expiration;
* role permissions;
* teacher–student access;
* duplicate word assignment;
* spaced repetition;
* exercise answer validation;
* statistics;
* teacher dashboard.

---

## Future Improvements

Possible future improvements:

* JWT authentication;
* refresh tokens;
* Redis caching;
* background tasks;
* AI-generated exercises;
* Docker deployment;
* CI/CD;
* monitoring;
* logging;
* production database configuration;
* mobile application using Flutter.

---

## License

This project is created for educational purposes and personal portfolio development.
