import pytest
import httpx
from module_26_fastapi.homework import app

@pytest.mark.asyncio
async def test_get_recipes():
    """
    Тест для проверки получения списка всех рецептов.
    Отправляет GET-запрос на эндпоинт /recipes и проверяет:
    - Статус-код ответа должен быть 200.
    - Ответ должен быть списком.
    """
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/recipes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_inf():
    """
    Тест для проверки получения информации о конкретном рецепте.
    Проверяет успешное получение существующего рецепта и
    обработку ошибки для несуществующего рецепта.
    """
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/recipes/фондю")
        if response.status_code == 200:
            assert isinstance(response.json(), list)

        # Проверка обработки несуществующего рецепта
        response = await client.get("/recipes/аоаоаоа")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Рецепт с ID Неизвестный_рецепт не найден."
        }


@pytest.mark.asyncio
async def test_record_recipe():
    """
    Тест для проверки возможности создания нового рецепта.
    Отправляет POST-запрос на эндпоинт /create_recipes с
    тестовыми данными и проверяет успешное создание рецепта.
    """
    test_data = {
        "name_recipe": "Фондю",
        "cooking_time": 30,
        "list_ingredients": "Сыр Вино Хлеб",
        "description": "Национальное горячее блюдо Швейцарии"
    }
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        responce = await client.post("/create_recipes", json=test_data)  # Передаем данные рецепта
        assert responce.status_code == 200
        assert responce.json() == {"message": "Рецепт успешно создан.", "data": test_data}


@pytest.mark.asyncio
async def test_validation_exception_handler():
    """
    Тест для проверки обработки ошибок валидации данных при создании рецепта.
    Проверяет, что отсутствие обязательного поля приводит к ошибке валидации.
    """
    invalid_data = {
        "cooking_time": 30,  # Пропущено поле "name_recipe"
        "list_ingredients": "Сыр Вино Хлеб",
        "description": "Национальное горячее блюдо Швейцарии"
    }
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/create_recipes", json=invalid_data)
        assert response.status_code == 422
        assert "detail" in response.json()
        assert response.json()["reason"] == "Ошибка валидации данных ввода"

@pytest.mark.asyncio
async def test_delete_recipe():
    """
    Тест для проверки возможности удаления рецепта.
    Проверяет создание, удаление и успешную проверку отсутствия рецепта.
    """
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        recipe_data = {
            "name_recipe": "фондю",
            "cooking_time": 30,
            "list_ingredients": "Сыр Вино Хлеб",
            "description": "Национальное горячее блюдо Швейцарии"
        }

        # Шаг 1: Создаем рецепт
        response = await client.post("/create_recipes", json=recipe_data)
        assert response.status_code == 200  # Проверяем, что рецепт успешно создан

        # Шаг 2: Удаляем рецепт
        response = await client.delete("/delete_recipe/фондю")
        assert response.status_code == 200
        assert response.json() == {"message": "Рецепт успешно удалён."}

        # Шаг 3: Проверяем, что рецепт был удалён
        response = await client.get("/recipes/фондю")
        assert response.status_code == 404
        assert response.json() == {"detail": "Рецепт с ID фондю не найден."}

        # Шаг 4: Проверяем, что несуществующий рецепт возвращает 404
        response = await client.delete("/delete_recipe/аоаоаоа")
        assert response.status_code == 404
        assert response.json() == {"detail": "Рецепт с ID аоаоаоа не найден."}


