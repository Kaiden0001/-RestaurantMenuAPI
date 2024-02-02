from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish_model import Dish, DishModel
from src.menu.models.menu_model import Menu, MenuModel
from src.menu.models.submenu_model import Submenu, SubmenuModel


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_menu_by_id(self, menu_id: UUID) -> MenuModel:
        """
        Получение меню по его уникальному идентификатору.

        :param menu_id: Уникальный идентификатор меню (UUID).
        :return: Модель данных MenuModel или None, если меню не найдено.
        """
        query: Select = select(Menu).where(Menu.id == menu_id)
        result: Result = await self.session.execute(query)
        return result.scalar()

    async def get_submenu_by_id(self, submenu_id: UUID) -> SubmenuModel:
        """
        Получение подменю по его уникальному идентификатору.

        :param submenu_id: Уникальный идентификатор подменю (UUID).
        :return: Модель данных SubmenuModel или None, если подменю не найдено.
        """
        query: Select = select(Submenu).where(Submenu.id == submenu_id)
        result: Result = await self.session.execute(query)
        return result.scalar()

    async def get_dish_by_id(self, dish_id: UUID) -> DishModel:
        """
        Получение блюда по его уникальному идентификатору.

        :param dish_id: Уникальный идентификатор блюда (UUID).
        :return: Модель данных DishModel или None, если блюдо не найдено.
        """
        query: Select = select(Dish).where(Dish.id == dish_id)
        result: Result = await self.session.execute(query)
        return result.scalar()
