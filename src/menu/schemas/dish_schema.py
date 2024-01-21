from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    """
        Основная модель данных для блюда.
    """
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    """
        Модель данных для создания нового блюда.
    """
    id: UUID | None = None


class DishUpdate(DishBase):
    """
        Модель данных для обновления информации о блюде.
    """
    pass
