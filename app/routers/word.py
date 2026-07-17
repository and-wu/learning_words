from fastapi import APIRouter, Depends, Response, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_word_service
from app.models.user import User
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


@router.post(
    "",
    response_model=WordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create word",
)
def create_word(
    data: CreateWordRequest,
    current_user: User = Depends(get_current_user),
    service: WordService = Depends(get_word_service),
):
    return service.create(
        data=data,
        created_by=current_user.id,
    )


@router.get(
    "",
    response_model=list[WordResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all words",
)
def get_words(
    service: WordService = Depends(get_word_service),
):
    return service.get_all()


@router.get(
    "/{word_id}",
    response_model=WordResponse,
    status_code=status.HTTP_200_OK,
    summary="Get word by id",
)
def get_word(
    word_id: int,
    service: WordService = Depends(get_word_service),
):
    return service.get_by_id(word_id)


@router.patch(
    "/{word_id}",
    response_model=WordResponse,
    status_code=status.HTTP_200_OK,
    summary="Update word",
)
def update_word(
    word_id: int,
    data: UpdateWordRequest,
    service: WordService = Depends(get_word_service),
):
    return service.update(
        word_id=word_id,
        data=data,
    )


@router.delete(
    "/{word_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete word",
)
def delete_word(
    word_id: int,
    service: WordService = Depends(get_word_service),
):
    service.delete(word_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)