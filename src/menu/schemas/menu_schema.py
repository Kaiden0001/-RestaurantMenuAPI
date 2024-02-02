from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    """Основная модель данных для меню."""
    title: str
    description: str


class MenuCreate(MenuBase):
    """Модель данных для создания нового меню."""
    id: UUID | None = None


class MenuUpdate(MenuBase):
    """Модель данных для обновления информации о меню."""
    pass
