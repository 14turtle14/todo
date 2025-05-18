import pytest
from unittest.mock import AsyncMock
from api.models.schemas.task_schema import TaskCreate
from api.services.task_service import TaskService

@pytest.mark.asyncio
async def test_create_task(mocker):
    # Мокируем сессию БД
    mock_db = AsyncMock()
    mock_user = AsyncMock(id=1)

    # Мокируем вызовы к БД
    mocker.patch("app.crud.task.create_task", return_value={"id": 1, "title": "Test"})

    # Вызываем сервис
    task_data = TaskCreate(title="Test")
    result = await TaskService.create_task(mock_db, task_data, mock_user)

    # Проверяем результат
    assert result["title"] == "Test"
    mock_db.commit.assert_called_once()