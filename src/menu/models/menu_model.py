from typing import TYPE_CHECKING

from pydantic import UUID4, BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.menu.models.base import Base

if TYPE_CHECKING:
    from src.menu.models.submenu_model import Submenu


class Menu(Base):
    """Модель базы данных для меню."""
    __tablename__ = 'menu'

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    submenus: Mapped[list['Submenu']] = relationship('Submenu', back_populates='menu')


class MenuModel(BaseModel):
    """Модель данных (Pydantic) для меню."""
    id: UUID4
    title: str
    description: str


class MenuDetailModel(MenuModel):
    """Модель данных (Pydantic) для меню с доп. полями."""
    submenus_count: int
    dishes_count: int
