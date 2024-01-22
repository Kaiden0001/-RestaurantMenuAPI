from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import (
    Select,
    select,
    func,
    Result,
    Update,
    update,
    Delete,
    delete
)
from src.menu.models.dish_model import Dish
from src.menu.models.menu_model import MenuModel, Menu, MenuDetailModel
from src.menu.models.submenu_model import Submenu
from src.menu.repositories.base_repository import BaseRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate


class MenuRepository(BaseRepository):
    async def get_menus(self) -> list[MenuModel]:
        """
        Получение списка меню.

        :return: Список моделей данных MenuModel.
        """
        query: Select = select(Menu)
        result: Result = await self.session.execute(query)
        result_all: list[MenuModel] = result.scalars().all()
        return result_all

    async def get_menu_detail(self, menu_id: UUID) -> MenuDetailModel | None:
        """
        Получение подробной информации о конкретном меню.

        :param menu_id: Уникальный идентификатор меню (UUID).
        :return: Модель данных MenuDetailModel или None, если меню не найдено.
        :raise HTTPException: Исключение с кодом 404, если меню не найдено.
        """
        subquery: Any = select(
            Dish.submenu_id,
            func.count(Dish.id).label('submenu_dish_count')
        ).group_by(Dish.submenu_id).subquery()

        menu_query: Select = select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(Submenu.id).label('submenu_count'),
            func.sum(subquery.c.submenu_dish_count).label('total_dish_count')
        ).select_from(Menu).outerjoin(Submenu).outerjoin(subquery, Submenu.id == subquery.c.submenu_id).where(
            Menu.id == menu_id).group_by(Menu.id)

        result_menu: Result = await self.session.execute(menu_query)
        menu: Any = result_menu.first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        menu_detail: MenuDetailModel = MenuDetailModel(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=int(menu.submenu_count) if menu.submenu_count is not None else 0,
            dishes_count=int(menu.total_dish_count) if menu.total_dish_count is not None else 0
        )
        return menu_detail

    async def create_menu(self, menu_create: MenuCreate) -> MenuModel:
        """
        Создание нового меню.

        :param menu_create: Схема данных для создания нового меню.
        :return: Модель данных созданного меню.
        """
        db_menu: Menu = Menu(**menu_create.model_dump())
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)

        return db_menu

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuModel | None:
        """
        Обновление информации о меню.

        :param menu_id: Уникальный идентификатор меню, которое нужно обновить.
        :param menu_update: Схема данных для обновления информации о меню.
        :return: Модель обновленного меню.
        :raise HTTPException: Исключение с кодом 404, если меню не найдено.
        """
        existing_menu: Any = await self.get_menu_by_id(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=404, detail="Menu not found")

        query: Update = update(Menu).where(Menu.id == menu_id).values(**menu_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        return await self.get_menu_by_id(menu_id)

    async def delete_menu(self, menu_id: UUID) -> MenuModel | None:
        """
        Удаление меню.

        :param menu_id: Уникальный идентификатор меню (UUID).
        :return: Модель данных удаленного меню.
        :raise HTTPException: Исключение с кодом 404, если меню не найдено.
        """
        existing_menu: MenuModel = await self.get_menu_by_id(menu_id)

        if not existing_menu:
            raise HTTPException(status_code=404, detail='menu not found')

        query: Delete = delete(Menu).where(Menu.id == menu_id)
        await self.session.execute(query)
        await self.session.commit()

        return existing_menu
