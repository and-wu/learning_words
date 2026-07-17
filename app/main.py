from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.teacher_student_request import router as teacher_student_request_router
from app.routers.teacher_student import router as teacher_student_router
from app.routers.word import router as word_router
from app.routers.student_word import router as student_word_router
from app.routers.exercise import router as exercise_router
from app.routers.statistics import router as statistics_router
from app.routers.teacher_dashboard import router as teacher_dashboard_router
app = FastAPI(
    title="Learning Words API",
    description="Backend API for Korean vocabulary learning.",
    version="0.1.0",
)

def include_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(teacher_student_request_router)
    app.include_router(teacher_student_router)
    app.include_router(word_router)
    app.include_router(student_word_router)
    app.include_router(exercise_router)
    app.include_router(statistics_router)
    app.include_router(teacher_dashboard_router)

include_routers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Learning Words API is running!"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
    }