import uuid

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from src.database import Base
from src.menu.models.dish_model import Dish


class Submenu(Base):
    """Модель базы данных для подменю."""
    __tablename__ = 'submenu'

    id: UUID4 = Column(UUID, primary_key=True, default=uuid.uuid4)
    title: str = Column(String, nullable=False, unique=True)
    description: str = Column(String, nullable=False)
    menu_id: UUID4 = Column(UUID, ForeignKey('menu.id', ondelete='CASCADE'),
                            nullable=False)

    menu: Mapped[list['Menu']] = relationship('Menu',
                                              back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship('Dish',
                                                back_populates='submenu')


class SubmenuModel(BaseModel):
    """Модель данных (Pydantic) для подменю."""
    id: UUID4
    title: str
    description: str
    menu_id: UUID4


class SubmenuDetailModel(SubmenuModel):
    """Модель данных (Pydantic) для подменю с доп. полям."""
    dishes_count: int
