import asyncio
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from module_30_ci_linters.homework.app.models import Table1, Table2, Base
from sqlalchemy.future import select
from sqlalchemy import desc, asc
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from module_30_ci_linters.homework.app.schemas import CookBook

# Создание экземпляра FastAPI
app = FastAPI()

# URL базы данных SQLite
database_url = "sqlite+aiosqlite:///cookbook.db"
# Создание асинхронного движка базы данных
engine = create_async_engine(database_url, echo=True)
# Создание сессии для работы с базой данных
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# Базовый класс для объявляемых моделей
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Создает асинхронную сессию базы данных.

    Используется в зависимости для маршрутов, которые требуют доступ к базе данных.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.
    """
    async with async_session() as session:
        yield session


@app.get("/recipes")
async def get_recipes(db: AsyncSession = Depends(get_db)):
    """
    Получает список всех рецептов.

    Рецепты сортируются по количеству просмотров (по убыванию) и времени приготовления (по возрастанию).

    Args:
        db (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        list: Список всех рецептов в формате JSON.
    """
    result = await db.execute(
        select(Table1).order_by(desc(Table1.views), asc(Table1.cooking_time))
    )
    records = result.scalars().all()
    return records


@app.get("/recipes/{recipe_id}")
async def get_inf(recipe_id: str, db: AsyncSession = Depends(get_db)):
    """
    Получает информацию о конкретном рецепте по его ID.

    Увеличивает счетчик просмотров для данного рецепта.

    Args:
        recipe_id (str): ID рецепта.
        db (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        list: Список деталей рецепта в формате JSON.

    Raises:
        HTTPException: Если рецепт с указанным ID не найден (404).
    """
    result_table2 = await db.execute(select(Table2).filter(Table2.name_recipe.contains(recipe_id)))
    records = result_table2.scalars().all()
    if not records:
        raise HTTPException(status_code=404, detail=f"Рецепт с ID {recipe_id} не найден.")

    try:
        result_table1 = await db.execute(
            select(Table1).filter(Table1.title.contains(recipe_id))
        )
        recipe_record = result_table1.scalars().first()
        if recipe_record:
            recipe_record.views += 1
            await db.commit()
    except Exception as e:
        print(f"Ошибка при обновлении счетчика просмотров: {e}")

    return records


@app.post("/create_recipes")
async def record_recipe(recipe: CookBook, db: AsyncSession = Depends(get_db)):
    """
    Создает новый рецепт и сохраняет его в базу данных.

    Args:
        recipe (CookBook): Объект рецепта, который необходимо сохранить.
        db (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        dict: Сообщение об успешном создании рецепта.
    """
    new_recipe_to_table2 = Table2(**recipe.model_dump())
    db.add(new_recipe_to_table2)
    await db.commit()

    table1_data = {
        "title": recipe.name_recipe,
        "views": 0,
        "cooking_time": recipe.cooking_time
    }
    new_recipe_to_table1 = Table1(**table1_data)
    db.add(new_recipe_to_table1)
    await db.commit()

    return {"message": "Рецепт успешно создан.", "data": recipe}


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Обработчик ошибок валидации данных ввода.

    Args:
        request (Request): HTTP-запрос, который вызвал ошибку.
        exc (ValidationError): Исключение, содержащее ошибки валидации.

    Returns:
        JSONResponse: Ответ с ошибками валидации и соответствующим статусом.
    """
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(),
                 "reason": "Ошибка валидации данных ввода"},
    )


@app.delete("/delete_recipe/{recipe_id}")
async def delete_recipe(recipe_id: str, db: AsyncSession = Depends(get_db)):
    """
    Удаляет рецепт по его ID из базы данных.

    Args:
        recipe_id (str): ID рецепта, который нужно удалить.
        db (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        dict: Сообщение об успешном удалении рецепта.

    Raises:
        HTTPException: Если рецепт с указанным ID не найден (404).
    """
    result = await db.execute(select(Table2).where(Table2.name_recipe == recipe_id))
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(status_code=404, detail=f"Рецепт с ID {recipe_id} не найден.")

    await db.delete(recipe)
    await db.commit()

    result_table1 = await db.execute(select(Table1).where(Table1.title == recipe_id))
    recipe_table1 = result_table1.scalar_one_or_none()

    if recipe_table1:
        await db.delete(recipe_table1)

    await db.commit()

    return {"message": "Рецепт успешно удалён."}


async def init_main():
    """
    Инициализирует базу данных, создавая все таблицы.

    Вызывается при запуске приложения.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Точка входа для запуска приложения
if __name__ == "__main__":
    asyncio.run(init_main())

