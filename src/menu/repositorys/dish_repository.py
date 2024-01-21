from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import (
    Select,
    select,
    Update,
    update,
    Delete,
    delete,
    Result
)

from src.menu.models.dish_model import Dish, DishModel
from src.menu.repositorys.base_repository import BaseRepository
from src.menu.schemas.dish_schema import DishUpdate, DishCreate


class DishRepository(BaseRepository):

    async def get_dish(self, dish_id: UUID) -> DishModel | None:
        """
        Получение информации о блюде по его уникальному идентификатору.

        :param dish_id: Уникальный идентификатор блюда (UUID).
        :return: Модель данных DishModel или None, если блюдо не найдено.
        :raise HTTPException: Исключение с кодом 404, если блюдо не найдено.
        """
        db_dish: Any = await self.get_dish_by_id(dish_id)
        if not db_dish:
            raise HTTPException(status_code=404, detail="dish not found")

        return db_dish

    async def get_dishes(self, submenu_id: UUID) -> list[DishModel]:
        """
        Получение списка блюд для указанного подменю.

        :param submenu_id: Уникальный идентификатор подменю (UUID).
        :return: Список моделей данных DishModel.
        """
        query: Select = select(Dish).where(Dish.submenu_id == submenu_id)
        result: Result = await self.session.execute(query)

        return result.scalars().all()

    async def update_dish(self, dish_id: UUID,
                          dish_update: DishUpdate) -> DishModel | None:
        """
        Обновление информации о блюде.

        :param dish_id: Уникальный идентификатор блюда, которое нужно обновить.
        :param dish_update: Схема данных для обновления информации о блюде.
        :return: Модель обновленного блюда.
        :raise HTTPException: Исключение с кодом 404, если блюдо не найдено.
       """
        existing_dish: Any = await self.get_dish_by_id(dish_id)
        if not existing_dish:
            raise HTTPException(status_code=404, detail="dish not found")
        del existing_dish

        query: Update = update(Dish).where(Dish.id == dish_id).values(
            **dish_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        return await self.get_dish_by_id(dish_id)

    async def create_dish(self, submenu_id: UUID,
                          dish_create: DishCreate) -> DishModel | None:
        """
        Создание нового блюда в указанном подменю.

        :param submenu_id: Уникальный идентификатор подменю (UUID).
        :param dish_create: Схема данных для создания нового блюда.
        :return: Модель данных созданного блюда.
        """
        db_dish: Dish = Dish(**dish_create.model_dump(), submenu_id=submenu_id)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)

        return db_dish

    async def delete_dish(self, dish_id: UUID) -> DishModel | None:
        """
        Удаление блюда по его уникальному идентификатору.

        :param dish_id: Уникальный идентификатор блюда (UUID).
        :return: Модель данных удаленного блюда.
        :raise HTTPException: Исключение с кодом 404, если блюдо не найдено.
        """
        db_dish: DishModel | None = await self.get_dish_by_id(dish_id)

        if not db_dish:
            raise HTTPException(status_code=404, detail="Dish not found")

        query: Delete = delete(Dish).where(Dish.id == dish_id)
        await self.session.execute(query)
        await self.session.commit()

        return db_dish
