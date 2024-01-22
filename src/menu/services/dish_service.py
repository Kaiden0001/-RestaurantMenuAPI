from uuid import UUID

from src.menu.models.dish_model import DishModel
from src.menu.repositories.dish_repository import DishRepository
from src.menu.schemas.dish_schema import DishUpdate, DishCreate


class DishService:
    def __init__(self, dish_repository: DishRepository):
        self.dish_repository = dish_repository

    async def get_dishes(self, submenu_id: UUID) -> list[DishModel] | None:
        """
        Получить список блюд подменю.

        :param submenu_id: Идентификатор подменю.
        :return: Список блюд подменю или None, если подменю не найдено.

        """
        return await self.dish_repository.get_dishes(submenu_id)

    async def get_dish(self, dish_id: UUID) -> DishModel | None:
        """
        Получить информацию о блюде по его идентификатору.

        :param dish_id: Идентификатор блюда.
        :return: Модель блюда или None, если блюдо не найдено.

        """
        return await self.dish_repository.get_dish(dish_id)

    async def create_dish(self, submenu_id: UUID,
                          dish_update: DishCreate) -> DishModel:
        """
        Создать новое блюдо в подменю.

        :param submenu_id: Идентификатор подменю.
        :param dish_update: Данные для создания блюда.
        :return: Модель созданного блюда.

        """
        return await self.dish_repository.create_dish(submenu_id, dish_update)

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate):
        """
        Обновить информацию о блюде.

        :param dish_id: Идентификатор блюда, которое нужно обновить.
        :param dish_update: Схема данных для обновления информации о блюде.

        """
        return await self.dish_repository.update_dish(dish_id, dish_update)

    async def delete_dish(self, dish_id: UUID) -> DishModel | None:
        """
        Удалить блюдо.

        :param dish_id: Идентификатор блюда, которое нужно удалить.
        :return: Модель удаленного блюда или None, если блюдо не найдено.

        """
        return await self.dish_repository.delete_dish(dish_id)
