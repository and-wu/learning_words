from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.routers.auth import router as auth_router
from app.routers.teacher_student_request import router as teacher_student_request_router
app = FastAPI(
    title="Learning Words API",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(teacher_student_request_router)

@app.get("/")
def root():
    return {
        "message": "Learning Words API is running!"
    }