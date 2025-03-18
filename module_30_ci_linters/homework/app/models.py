import asyncio
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import  declarative_base

# URL подключения к базе данных
database_url = "sqlite+aiosqlite:///cookbook.db"
engine = create_async_engine(database_url, echo=True)
Base = declarative_base()

class Table1(Base):
    """
    Модель таблицы для хранения основной информации о рецептах.

    Attributes:
        id (int): Уникальный идентификатор рецепта (первичный ключ).
        title (str): Название рецепта.
        views (int): Количество просмотров рецепта (по умолчанию 0).
        cooking_time (int): Время приготовления рецепта в минутах.
    """

    __tablename__ = 'name_list_recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    views = Column(Integer, default=0, nullable=False)
    cooking_time = Column(Integer, nullable=False)

class Table2(Base):
    """
    Модель таблицы для хранения полной информации о рецептах.

    Attributes:
        id (int): Уникальный идентификатор рецепта (первичный ключ).
        name_recipe (str): Название рецепта.
        cooking_time (int): Время приготовления рецепта в минутах.
        list_ingredients (str): Список ингредиентов для рецепта.
        description (str): Описание рецепта.
    """

    __tablename__ = 'full_info_recipes'

    id = Column(Integer, primary_key=True, index=True)
    name_recipe = Column(String, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    list_ingredients = Column(String, nullable=False)
    description = Column(String, nullable=False)

async def init_db():
    """
    Инициализация базы данных: создание всех таблиц, определенных в моделях.

    Использует асинхронный контекстный менеджер для выполнения
    операции создания таблиц в базе данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
