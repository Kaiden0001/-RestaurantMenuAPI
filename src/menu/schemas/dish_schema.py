from pydantic import BaseModel


class DishBase(BaseModel):
    """Основная модель данных для блюда."""
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    """Модель данных для создания нового блюда."""
    pass


class DishUpdate(DishBase):
    """Модель данных для обновления информации о блюде."""
    pass
