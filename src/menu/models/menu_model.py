import uuid

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import Mapped, relationship

from src.database import Base
from src.menu.models.submenu_model import Submenu


class Menu(Base):
    """
    Модель базы данных для меню.
    """
    __tablename__ = 'menu'

    id: UUID4 = Column(UUID, primary_key=True, default=uuid.uuid4)
    title: str = Column(String, nullable=False, unique=True)
    description: str = Column(String, nullable=False)

    submenus: Mapped[list['Submenu']] = relationship('Submenu', back_populates='menu')


class MenuModel(BaseModel):
    """
    Модель данных (Pydantic) для меню.
    """
    id: UUID4
    title: str
    description: str


class MenuDetailModel(MenuModel):
    """
    Модель данных (Pydantic) для меню с доп. полями.
    """
    submenus_count: int
    dishes_count: int
