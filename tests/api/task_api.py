from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_create_task(async_client: AsyncClient):
    # 1. Аутентификация (если нужно)
    auth_data = {"email": "test@example.com", "password": "123"}
    await async_client.post("/auth/signup", json=auth_data)
    login = await async_client.post("/auth/login", data=auth_data)
    token = login.json()["access_token"]

    # 2. Создаём задачу
    task_data = {"title": "Test Task"}
    response = await async_client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

@pytest.mark.asyncio
async def test_delete_foreign_task(async_client: AsyncClient):
    # 1. Создаём двух пользователей
    user1 = {"email": "user1@test.com", "password": "123"}
    user2 = {"email": "user2@test.com", "password": "123"}
    await async_client.post("/auth/signup", json=user1)
    await async_client.post("/auth/signup", json=user2)

    # 2. User1 создаёт задачу
    login = await async_client.post("/auth/login", data=user1)
    token_user1 = login.json()["access_token"]
    task = await async_client.post("/tasks/", json={"title": "Task"}, headers={"Authorization": f"Bearer {token_user1}"})
    task_id = task.json()["id"]

    # 3. User2 пытается удалить задачу User1
    login = await async_client.post("/auth/login", data=user2)
    token_user2 = login.json()["access_token"]
    response = await async_client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_user2}"}
    )
    assert response.status_code == 403  # Forbidden