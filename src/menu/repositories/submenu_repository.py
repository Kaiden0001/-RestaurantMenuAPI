from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import Delete, Result, Select, Update, delete, func, select, update

from src.menu.models.dish_model import Dish
from src.menu.models.submenu_model import Submenu, SubmenuDetailModel, SubmenuModel
from src.menu.repositories.base_repository import BaseRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate


class SubmenuRepository(BaseRepository):
    async def get_submenus(self, menu_id: UUID) -> list[SubmenuModel]:
        """
        Получение списка подменю для конкретного меню.

        :param menu_id: Уникальный идентификатор меню, для которого нужно
        получить подменю.
        :return: Список моделей данных SubmenuModel или None, если подменю не
        найдено.
        """
        query: Select = select(Submenu).where(Submenu.menu_id == menu_id)
        result: Result = await self.session.execute(query)
        result_all: list[SubmenuModel] = result.scalars().all()
        return result_all

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuModel:
        """
        Создание нового подменю.

        :param menu_id: Уникальный идентификатор меню, к которому привязывается
         подменю.
        :param submenu_create: Схема данных для создания нового подменю.
        :return: Модель данных созданного подменю.
        """
        db_submenu: Submenu = Submenu(menu_id=menu_id, **submenu_create.model_dump())
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)

        return db_submenu

    async def get_submenu_detail(self, menu_id: UUID, submenu_id: UUID) -> SubmenuDetailModel:
        """
        Получение подробной информации о конкретном подменю.

        :param menu_id: Уникальный идентификатор меню, к которому привязано
        подменю.
        :param submenu_id: Уникальный идентификатор подменю (UUID).
        :return: Модель данных SubmenuDetailModel или None, если подменю не
        найдено.
        :raise HTTPException: Исключение с кодом 404, если подменю не найдено.
        """
        submenu_query: Select = select(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            func.count(Dish.id).label('dish_count')
        ).select_from(Submenu). \
            outerjoin(Dish, Submenu.id == Dish.submenu_id). \
            where(Submenu.menu_id == menu_id, Submenu.id == submenu_id). \
            group_by(Submenu.id)

        result_submenu: Result = await self.session.execute(submenu_query)
        submenu: Any = result_submenu.first()

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        submenu_detail: SubmenuDetailModel = SubmenuDetailModel(
            id=submenu.id,
            title=submenu.title,
            menu_id=menu_id,
            description=submenu.description,
            dishes_count=int(submenu.dish_count) if submenu.dish_count is not None else 0
        )

        return submenu_detail

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate) -> SubmenuModel:
        """
        Обновление информации о подменю.

        :param menu_id: Уникальный идентификатор меню, к которому привязано подменю.
        :param submenu_id: Уникальный идентификатор подменю, которое нужно обновить.
        :param submenu_update: Схема данных для обновления информации о подменю.
        :return: Модель обновленного подменю.
        :raise HTTPException: Исключение с кодом 404, если подменю не найдено.
        """
        existing_submenu: Any = await self.get_submenu_by_id(submenu_id)
        if not existing_submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        query: Update = update(Submenu).where(Submenu.menu_id == menu_id,
                                              Submenu.id == submenu_id).values(**submenu_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        return await self.get_submenu_by_id(submenu_id)

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubmenuModel:
        """
        Удаление подменю.

        :param menu_id: Уникальный идентификатор меню, к которому привязано подменю.
        :param submenu_id: Уникальный идентификатор подменю (UUID).
        :return: Модель данных удаленного подменю.
        :raise HTTPException: Исключение с кодом 404, если подменю не найдено.
        """
        existing_submenu: SubmenuModel = await self.get_submenu_by_id(submenu_id)

        if not existing_submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        query: Delete = delete(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
        await self.session.execute(query)
        await self.session.commit()

        return existing_submenu
