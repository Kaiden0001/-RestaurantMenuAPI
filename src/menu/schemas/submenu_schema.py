from pydantic import BaseModel


class SubmenuBase(BaseModel):
    """Основная модель данных для подменю."""
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    """Модель данных для создания нового подменю."""
    pass


class SubmenuUpdate(SubmenuBase):
    """Модель данных для обновления информации о подменю."""
    pass
