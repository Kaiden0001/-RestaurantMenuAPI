from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.menu.models.base import Base

if TYPE_CHECKING:
    from src.menu.models.submenu_model import Submenu


class Dish(Base):
    """Модель базы данных для блюда."""
    __tablename__ = 'dish'

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    submenu_id: Mapped[str] = mapped_column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'))

    submenu: Mapped[list['Submenu']] = relationship('Submenu', back_populates='dishes')


class DishModel(BaseModel):
    """Модель данных (Pydantic) для блюда."""
    id: UUID4
    title: str
    description: str
    price: Decimal
    submenu_id: UUID4


class DishDiscountModel(DishModel):
    discount: Decimal | None
