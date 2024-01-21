from uuid import UUID

from src.menu.models.menu_model import MenuModel, MenuDetailModel
from src.menu.repositorys.menu_repository import MenuRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate


class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    async def get_menus(self) -> list[MenuModel]:
        """
        Получить список меню.

        :return: Список моделей меню.

        """
        return await self.menu_repository.get_menus()

    async def create_menu(self, menu_create: MenuCreate) -> MenuModel | None:
        """
        Создать новое меню.

        :param menu_create: Данные для создания меню.
        :return: Модель созданного меню или None, если не удалось создать.

        """
        return await self.menu_repository.create_menu(menu_create)

    async def get_menu(self, menu_id: UUID) -> MenuDetailModel | None:
        """
        Получить детальную информацию о меню.

        :param menu_id: Идентификатор меню.
        :return: Модель детальной информации о меню или None, если меню не найдено.

        """
        return await self.menu_repository.get_menu_detail(menu_id)

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuModel | None:
        """
        Обновить информацию о меню.

        :param menu_id: Идентификатор меню, которое нужно обновить.
        :param menu_update: Схема данных для обновления информации о меню.
        :return: Модель обновленного меню или None, если меню не найдено.

        """
        return await self.menu_repository.update_menu(menu_id, menu_update)

    async def delete_menu(self, menu_id: UUID) -> MenuModel | None:
        """
        Удалить меню.

        :param menu_id: Идентификатор меню, которое нужно удалить.
        :return: Модель удаленного меню или None, если меню не найдено.

        """
        return await self.menu_repository.delete_menu(menu_id)