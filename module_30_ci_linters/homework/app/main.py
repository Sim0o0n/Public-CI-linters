import asyncio
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import asc, desc, update
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.future import select

from .models import Base, Table1, Table2
from .schemas import CookBook

# Создание экземпляра FastAPI
app = FastAPI()

# URL базы данных SQLite
database_url = "sqlite+aiosqlite:///cookbook.db"
# Создание асинхронного движка базы данных
engine = create_async_engine(database_url, echo=True)
# Создание сессии для работы с базой данных
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, autoflush=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


# Создаём зависимость заранее для устранения ошибки B008
db_dependency = Depends(get_db)


@app.get("/recipes")
async def get_recipes(db: AsyncSession = db_dependency):
    result = await db.execute(
        select(Table1).order_by(desc(Table1.views), asc(Table1.cooking_time))
    )
    return result.scalars().all()


@app.get("/recipes/{recipe_id}")
async def get_inf(recipe_id: str, db: AsyncSession = db_dependency):
    result_table2 = await db.execute(
        select(Table2).where(Table2.name_recipe.contains(recipe_id))
    )
    records = result_table2.scalars().all()

    if not records:
        raise HTTPException(
            status_code=404, detail=f"Рецепт с ID {recipe_id} не найден."
        )

    result_table1 = await db.execute(
        select(Table1).where(Table1.title.contains(recipe_id))
    )
    recipe_record = result_table1.scalars().first()

    if recipe_record:
        await db.execute(
            update(Table1)
            .where(Table1.title == recipe_record.title)
            .values(views=recipe_record.views + 1)
        )
        await db.commit()

    return records


@app.post("/create_recipes")
async def record_recipe(recipe: CookBook, db: AsyncSession = db_dependency):
    new_recipe_to_table2 = Table2(**recipe.model_dump())
    db.add(new_recipe_to_table2)
    await db.commit()

    new_recipe_to_table1 = Table1(
        title=recipe.name_recipe, views=0, cooking_time=recipe.cooking_time
    )
    db.add(new_recipe_to_table1)
    await db.commit()

    return {"message": "Рецепт успешно создан.", "data": recipe}


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "reason": "Ошибка валидации данных"},
    )


@app.delete("/delete_recipe/{recipe_id}")
async def delete_recipe(recipe_id: str, db: AsyncSession = db_dependency):
    result = await db.execute(
    select(Table2).where(Table2.name_recipe == recipe_id)
)
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(
            status_code=404, detail=f"Рецепт с ID {recipe_id} не найден."
        )

    await db.delete(recipe)
    await db.commit()

    result_table1 = await db.execute(
    select(Table1).where(Table1.title == recipe_id)
)
    recipe_table1 = result_table1.scalar_one_or_none()

    if recipe_table1:
        await db.delete(recipe_table1)
        await db.commit()

    return {"message": "Рецепт успешно удалён."}


async def init_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_main())
