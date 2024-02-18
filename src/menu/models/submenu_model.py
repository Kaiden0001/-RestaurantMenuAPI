from typing import TYPE_CHECKING

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.menu.models.base import Base

if TYPE_CHECKING:
    from src.menu.models.dish_model import Dish
    from src.menu.models.menu_model import Menu


class Submenu(Base):
    """Модель базы данных для подменю."""
    __tablename__ = 'submenu'

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    menu_id: Mapped[str] = mapped_column(UUID, ForeignKey('menu.id', ondelete='CASCADE'))

    menu: Mapped[list['Menu']] = relationship('Menu', back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship('Dish', back_populates='submenu')


class SubmenuModel(BaseModel):
    """Модель данных (Pydantic) для подменю."""
    id: UUID4
    title: str
    description: str
    menu_id: UUID4


class SubmenuDetailModel(SubmenuModel):
    """Модель данных (Pydantic) для подменю с доп. полям."""
    dishes_count: int
