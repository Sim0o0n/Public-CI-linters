from pydantic import BaseModel, Field, field_validator


class CookBook(BaseModel):
    """
    Модель для представления рецепта в кулинарной книге.

    Attributes:
        id (int): Уникальный идентификатор рецепта.
        name_recipe (str): Название рецепта (не более 40 символов).
        cooking_time (int): Время приготовления в минутах.
        list_ingredients (str): Список ингредиентов, вводимый через пробел.
        description (str): Краткое описание рецепта (не более 100 символов).
    """

    id: int
    name_recipe: str = Field(
        max_length=40, description="Название рецепта (не больше 40 символов)"
    )
    cooking_time: int = Field(description="Время приготовления (в минутах)")
    list_ingredients: str = Field(
        description="Список ингредиентов (ввод осуществляется через пробел)"
    )
    description: str = Field(
        max_length=100, description="Описание (не более 100 символов)"
    )

    @field_validator("list_ingredients", mode="before")
    def convert_ingredients(cls, value: str) -> str:
        """
        Преобразует список ингредиентов из строки, разделенной пробелами,
        в строку, разделенную запятыми.

        Args:
            cls: Класс, к которому применяется валидатор.
            value (str): Входное значение для проверки.

        Returns:
            str: Строка с ингредиентами, разделенными запятыми.

        Raises:
            ValueError: Если значение не является строкой.
        """
        if isinstance(value, str):
            ingredients_list = value.split()
            return ", ".join(ingredients_list)
        return value
