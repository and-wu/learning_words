from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_word_service
from app.models.user import User
from app.repositories.word_repository import WordRepository
from app.schemas.words import (
    CreateWordRequest,
    UpdateWordRequest,
    WordResponse,
)
from app.services.word_service import WordService

router = APIRouter(
    prefix="/words",
    tags=["Words"],
)

@router.post("",response_model=WordResponse)
def create_word(
    data: CreateWordRequest,
    current_user: User = Depends(get_current_user),
    service: WordService = Depends(
        get_word_service,
    ),
):

    return service.create(
        data=data,
        created_by=current_user.id,
    )

@router.get("", response_model=list[WordResponse])
def get_words(service: WordService = Depends(
        get_word_service,
    )):

    return service.get_all()

@router.get("/{word_id}", response_model=WordResponse)
def get_word(
    word_id: int,
    service: WordService = Depends(
        get_word_service,
    ),
):

    return service.get_by_id(word_id)

@router.patch("/{word_id}", response_model=WordResponse)
def update_word(
    word_id: int,
    data: UpdateWordRequest,
    service: WordService = Depends(
        get_word_service,
    ),
):

    return service.update(
        word_id=word_id,
        data=data,
    )

@router.delete("/{word_id}")
def delete_word(
        word_id: int,
        service: WordService = Depends(
            get_word_service,
        ),
):

    service.delete(word_id)

    return {
        "message": "Word deleted",
    }