from uuid import UUID

from src.menu.models.submenu_model import SubmenuModel, SubmenuDetailModel
from src.menu.repositorys.submenu_repository import SubmenuRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository):
        self.submenu_repository = submenu_repository

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuModel] | None:
        """
        Получить список подменю для конкретного меню.

        :param menu_id: Идентификатор меню.
        :return: Список моделей подменю или None, если меню не найдено.

        """
        return await self.submenu_repository.get_submenus(menu_id)

    async def create_submenu(self, menu_id: UUID,
                             submenu_create: SubmenuCreate) -> SubmenuModel | None:
        """
        Создать новое подменю.

        :param menu_id: Идентификатор меню, к которому привязывается подменю.
        :param submenu_create: Данные для создания подменю.
        :return: Модель созданного подменю или None, если не удалось создать.

        """
        return await self.submenu_repository.create_submenu(menu_id,
                                                            submenu_create)

    async def get_submenu_detail(self, menu_id: UUID,
                                 submenu_id: UUID) -> SubmenuDetailModel | None:
        """
        Получить детальную информацию о подменю.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :return: Модель детальной информации о подменю или None, если подменю
        не найдено.

        """
        return await self.submenu_repository.get_submenu_detail(menu_id,
                                                                submenu_id)

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID,
                             submenu_update: SubmenuUpdate) -> SubmenuModel | None:
        """
        Обновить информацию о подменю.

        :param menu_id: Идентификатор меню, к которому привязано подменю.
        :param submenu_id: Идентификатор подменю, которое нужно обновить.
        :param submenu_update: Схема данных для обновления информации о подменю.
        :return: Модель обновленного подменю или None, если подменю не найдено.

        """
        return await self.submenu_repository.update_submenu(menu_id,
                                                            submenu_id,
                                                            submenu_update)

    async def delete_submenu(self, menu_id: UUID,
                             submenu_id: UUID) -> SubmenuModel | None:
        """
        Удалить подменю.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю, которое нужно удалить.
        :return: Модель удаленного подменю или None, если подменю не найдено.

        """
        return await self.submenu_repository.delete_submenu(menu_id,
                                                            submenu_id)
