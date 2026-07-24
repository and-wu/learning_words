import pytest
from fastapi import HTTPException

from app.models import Word
from app.schemas.words import CreateWordRequest, UpdateWordRequest
from app.services.word_service import WordService


class FakeWordRepository:

    def __init__(
        self,
        words: list[Word] | None = None,
    ):
        self.words = words if words is None else []
        self.created_word: Word | None = None
        self.updated_word: Word | None = None
        self.deleted_word: Word | None = None

    def get_by_id(self, word_id: int) -> Word | None:

        for word in self.words:
            if word.id == word_id:
                return word

        return None

    def get_by_korean(self, korean: str) -> Word | None:

        for word in self.words:
            if word.korean == korean:
                return word

        return None

    def get_all(self) -> list[Word]:

        return list(self.words)

    def create(self, word: Word) -> Word:

        self.created_word = word
        self.words.append(word)

        return word

    def update(self, word: Word) -> Word:

        self.updated_word = word

        return word

    def delete(self, word: Word) -> None:

        self.deleted_word = word

@pytest.fixture
def word() -> Word:

    return Word(
        id=1,
        korean="안녕하세요",
        translation="Здравствуйте",
        part_of_speech="phrase",
        comment="Приветствие",
        created_by=1,
    )

# тест на успешное создание слова
def test_create_word_successfully():

    repository = FakeWordRepository()

    service = WordService(
        word_repository=repository,
    )

    data = CreateWordRequest(
        korean="감사합니다",
        translation="Спасибо",
        part_of_speech="verb",
        comment="Вежливая форма",
    )

    word = service.create(
        data=data,
        created_by=1,
    )

    assert word is repository.created_word

    assert word.korean == "감사합니다"

    assert word.translation == "Спасибо"

    assert word.part_of_speech == "verb"

    assert word.comment == "Вежливая форма"

    assert word.created_by == 1

# тест на попытку создания уже существующего слова
def test_create_word_with_existing_korean_raises_409(
    word: Word,
):

    repository = FakeWordRepository(
        words=[word],
    )

    service = WordService(
        word_repository=repository,
    )

    data = CreateWordRequest(
        korean="안녕하세요",
        translation="Привет",
    )

    with pytest.raises(HTTPException) as exception:

        service.create(
            data=data,
            created_by=1,
        )

    assert exception.value.status_code == 409

    assert exception.value.detail == "Word already exists"

    assert repository.created_word is None

# тест на успешное получение слова
def test_get_word_by_id_returns_word(
    word: Word,
):
    repository = FakeWordRepository(
        words=[word],
    )

    service = WordService(
        word_repository=repository,
    )

    result = service.get_by_id(
        word_id=1,
    )

    assert result is word

# тест на получение несуществующего слова
def test_get_word_by_id_when_word_not_found_raises_404():

    repository = FakeWordRepository()

    service = WordService(
        word_repository=repository,
    )

    with pytest.raises(HTTPException) as exception:

        service.get_by_id(
            word_id=999,
        )

    assert exception.value.status_code == 404

    assert exception.value.detail == "Word not found"

# тест проверяющий что WordService возвращает все слова, которые предоставил репозиторий
def test_get_all_returns_all_words(
    word: Word,
):

    second_word = Word(
        id=2,
        korean="감사합니다",
        translation="Спасибо",
        part_of_speech="verb",
        comment=None,
        created_by=1,
    )

    repository = FakeWordRepository(
        words=[word, second_word],
    )

    service = WordService(
        word_repository=repository,
    )

    result = service.get_all()

    assert result == [word, second_word]

# тест update - обновление только перевода
def test_update_word_translation_successfully(
    word: Word,
):
    repository = FakeWordRepository(
        words=[word],
    )

    service = WordService(
        word_repository=repository,
    )

    data = UpdateWordRequest(
        translation="Добрый день",
    )

    result = service.update(
        word_id=1,
        data=data,
    )

    assert result is word

    assert result.translation == "Добрый день"

    assert result.korean == "안녕하세요"

    assert result.part_of_speech == "phrase"

    assert result.comment == "Приветствие"

    assert repository.updated_word is word

# тест update - обновление самого слова на корейском
def test_update_word_korean_successfully(
    word: Word,
):
    repository = FakeWordRepository(
        words=[word],
    )

    service = WordService(
        word_repository=repository,
    )

    data = UpdateWordRequest(
        korean="안녕",
        translation="Здравствуйте",
    )

    result = service.update(
        word_id=1,
        data=data,
    )

    assert result is word

    assert result.korean == "안녕"

    assert result.translation == "Здравствуйте"

    assert repository.updated_word is word

# тест на попытку изменить Korean на уже существующее слово
def test_update_word_to_existing_korean_raises_409(
    word: Word,
):
    second_word = Word(
        id=2,
        korean="감사합니다",
        translation="Спасибо",
        part_of_speech="verb",
        comment=None,
        created_by=1,
    )

    repository = FakeWordRepository(
        words=[word, second_word],
    )

    service = WordService(
        word_repository=repository,
    )

    data = UpdateWordRequest(
        korean="감사합니다",
        translation="Здравствуйте",
    )

    with pytest.raises(HTTPException) as exception:
        service.update(
            word_id=1,
            data=data,
        )

    assert exception.value.status_code == 409

    assert exception.value.detail == "Word already exists"

    # Первое слово не должно измениться
    assert word.korean == "안녕하세요"

    # Репозиторий не должен обновить слово
    assert repository.updated_word is None

# тест на попытку изменить несуществующее слово
def test_update_nonexistent_word_raises_404():
    repository = FakeWordRepository()

    service = WordService(
        word_repository=repository,
    )

    data = UpdateWordRequest(
        korean="안녕",
        translation="Привет",
    )

    with pytest.raises(HTTPException) as exception:
        service.update(
            word_id=999,
            data=data,
        )

    assert exception.value.status_code == 404

    assert exception.value.detail == "Word not found"

    assert repository.updated_word is None

# тест на успешное удадение слова
def test_delete_word_successfully(
    word: Word,
):
    repository = FakeWordRepository(
        words=[word],
    )

    service = WordService(
        word_repository=repository,
    )

    result = service.delete(
        word_id=1,
    )

    assert result is None

    assert repository.deleted_word is word

# тест на попытку удалить несуществующее слово
def test_delete_nonexistent_word_raises_404():

    repository = FakeWordRepository()

    service = WordService(
        word_repository=repository,
    )

    with pytest.raises(HTTPException) as exception:
        service.delete(
            word_id=999,
        )

    assert exception.value.status_code == 404

    assert exception.value.detail == "Word not found"

    assert repository.deleted_word is None