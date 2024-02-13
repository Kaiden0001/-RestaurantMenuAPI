from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Delete, Result, Select, Update, delete, func, select, update
from sqlalchemy.orm import selectinload

from src.menu.models.dish_model import Dish
from src.menu.models.menu_model import Menu, MenuDetailModel, MenuModel
from src.menu.models.models_for_full_menu import (
    AllMenuModel,
    DishInfo,
    MenuInfo,
    SubmenuInfo,
)
from src.menu.models.submenu_model import Submenu
from src.menu.repositories.base_repository import BaseRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate


class MenuRepository(BaseRepository):

    async def _get_menu_query(self, menu_id: UUID | None = None) -> Result:
        """
        Формирует запрос для получения информации о меню.

        :param menu_id: Уникальный идентификатор меню (UUID). Если не указан, будет возвращена информация
        по всем меню.
        :return: Результат выполнения запроса.
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
        ).select_from(Menu).outerjoin(Submenu).outerjoin(subquery, Submenu.id == subquery.c.submenu_id)

        if menu_id:
            menu_query = menu_query.where(Menu.id == menu_id).group_by(Menu.id)
        else:
            menu_query = menu_query.group_by(Menu.id)

        return await self.session.execute(menu_query)

    @staticmethod
    def _create_menu_detail_model(menu: Any) -> MenuDetailModel:
        """
        Создает экземпляр модели данных MenuDetailModel на основе данных из запроса.

        :param menu: Результат запроса к таблице меню.
        :return: Экземпляр модели данных MenuDetailModel.
        """
        return MenuDetailModel(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=int(menu.submenu_count) if menu.submenu_count is not None else 0,
            dishes_count=int(menu.total_dish_count) if menu.total_dish_count is not None else 0
        )

    async def get_menus(self) -> list[MenuDetailModel]:
        """
        Получение списка меню.

        :return: Список моделей данных MenuModel.
        """
        result_menus: Result = await self._get_menu_query()
        menus: list[MenuDetailModel] = []

        for menu in result_menus:
            menu_detail: MenuDetailModel = self._create_menu_detail_model(menu)
            menus.append(menu_detail)

        return menus

    async def get_menu_detail(self, menu_id: UUID) -> MenuDetailModel:
        """
        Получение подробной информации о конкретном меню.

        :param menu_id: Уникальный идентификатор меню (UUID).
        :return: Модель данных MenuDetailModel.
        :raise HTTPException: Исключение с кодом 404, если меню не найдено.
        """
        result_menu: Result = await self._get_menu_query(menu_id)
        menu: Any = result_menu.first()

        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')

        menu_detail: MenuDetailModel = self._create_menu_detail_model(menu)
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

    async def get_full_menu(self) -> list[AllMenuModel]:
        menu_query: Select = (
            select(Menu)
            .options(
                selectinload(Menu.submenus)
                .selectinload(Submenu.dishes)
            )
        )
        result: Result = await self.session.execute(menu_query)
        menus = result.scalars().all()

        result_all: list[AllMenuModel] = [
            AllMenuModel(
                menu=MenuInfo(
                    id=menu.id,
                    title=menu.title,
                    description=menu.description,
                    submenus=[
                        SubmenuInfo(
                            id=submenu.id,
                            title=submenu.title,
                            description=submenu.description,
                            dishes=[
                                DishInfo(
                                    id=dish.id,
                                    title=dish.title,
                                    description=dish.description,
                                    price=dish.price
                                )
                                for dish in submenu.dishes
                            ]
                        )
                        for submenu in menu.submenus
                    ]
                )
            )
            for menu in menus
        ]
        return result_all

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuModel:
        """
        Обновление информации о меню.

        :param menu_id: Уникальный идентификатор меню, которое нужно обновить.
        :param menu_update: Схема данных для обновления информации о меню.
        :return: Модель обновленного меню.
        :raise HTTPException: Исключение с кодом 404, если меню не найдено.
        """
        existing_menu: Any = await self.get_menu_by_id(menu_id)
        if not existing_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Menu not found')

        query: Update = update(Menu).where(Menu.id == menu_id).values(**menu_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        return await self.get_menu_by_id(menu_id)

    async def delete_menu(self, menu_id: UUID | str) -> MenuModel:
        """
        Удаление меню.

        :param menu_id: Уникальный идентификатор меню (UUID).
        :return: Модель данных удаленного меню.
        :raise HTTPException: Исключение с кодом 404, если меню не найдено.
        """
        existing_menu: MenuModel = await self.get_menu_by_id(menu_id)

        if not existing_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')

        query: Delete = delete(Menu).where(Menu.id == menu_id)
        await self.session.execute(query)
        await self.session.commit()

        return existing_menu
