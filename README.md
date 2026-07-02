# Learning Words API

Backend API for learning Korean vocabulary with teacher-student collaboration, spaced repetition, and interactive exercises.

---

## About

Learning Words API is a REST backend for a Korean vocabulary learning platform.

The application allows teachers to assign words to students, students to study vocabulary using spaced repetition, and both teachers and students to monitor learning progress.

The project is built with a clean layered architecture:

* Routers
* Services
* Repositories
* SQLAlchemy ORM
* PostgreSQL

---

## Main Features

### Authentication

* User registration
* Login
* Logout
* Cookie-based authentication
* Current user endpoint

---

### Teacher ↔ Student Management

* Send teacher-to-student requests
* Send student-to-teacher requests
* Accept requests
* Reject requests
* View incoming requests
* View outgoing requests
* View teachers
* View students
* Deactivate teacher-student relationships

---

### Vocabulary

Planned functionality:

* Create words
* Edit words
* Delete words
* Browse dictionary

Each word contains:

* Korean text
* Translation
* Part of speech
* Comment
* Author

---

### Student Vocabulary

Planned functionality:

* Assign words to students
* Students add their own words
* Track learning progress
* Spaced repetition

---

### Exercises

Planned exercise types:

* Korean → Russian
* Russian → Korean
* Matching
* Sentence assembly

---

### Learning Statistics

Planned functionality:

* Review history
* Correct answers
* Wrong answers
* Current learning interval
* Next review date

---

## Technology Stack

* Python 3.13
* FastAPI
* SQLAlchemy 2.0
* PostgreSQL
* Alembic
* Pydantic v2
* bcrypt
* Uvicorn

---

## Project Structure

```text
app/
├── database/
├── dependencies/
├── enums/
├── models/
├── repositories/
├── routers/
├── schemas/
├── services/
└── main.py

alembic/
```

---

## Database

Current database includes:

* users
* sessions
* teacher_student_requests
* teacher_students

Planned tables:

* words
* student_words
* exercise_results

---

## Running the Project

### Install dependencies

```bash
uv sync
```

### Apply migrations

```bash
alembic upgrade head
```

### Start the application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Current Development Status

Implemented:

* Authentication
* Session management
* Teacher-student requests
* Teacher-student relationships

In progress:

* Words module

Planned:

* Student vocabulary
* Spaced repetition
* Exercises
* Learning statistics
* AI-generated exercises

---

## Future Improvements

* JWT authentication
* Refresh tokens
* Role-based permissions
* Redis caching
* Background tasks
* AI-generated exercises
* Docker deployment
* Automated testing
* CI/CD pipeline

---

## License

This project is created for educational purposes and personal portfolio development.
