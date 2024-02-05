from uuid import UUID

from aioredis import Redis

from src.menu.models.submenu_model import SubmenuDetailModel, SubmenuModel
from src.menu.repositories.submenu_repository import SubmenuRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate
from src.menu.services.cache_service import CacheService


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository, redis: Redis):
        self.submenu_repository = submenu_repository
        self.cache_service: CacheService = CacheService(redis)

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuDetailModel]:
        """
        Получить список подменю для конкретного меню.

        :param menu_id: Идентификатор меню.
        :return: Список моделей подменю.
        """
        cache_key: str = f'get_submenus:{menu_id}'
        result_cache: list[SubmenuDetailModel] | None = await self.cache_service.get_cache(cache_key)

        if result_cache:
            return result_cache

        result: list[SubmenuDetailModel] = await self.submenu_repository.get_submenus(menu_id)
        await self.cache_service.set_cache(cache_key=cache_key, result=result)
        return result

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuModel:
        """
        Создать новое подменю.

        :param menu_id: Идентификатор меню, к которому привязывается подменю.
        :param submenu_create: Данные для создания подменю.
        :return: Модель созданного подменю.
        """

        result: SubmenuModel = await self.submenu_repository.create_submenu(menu_id, submenu_create)
        await self.cache_service.delete_cache(f'/api/v1/menus/{menu_id}', f'get_submenus:{menu_id}')

        return result

    async def get_submenu_detail(self, url: str, menu_id: UUID, submenu_id: UUID) -> SubmenuDetailModel:
        """
        Получить детальную информацию о подменю.

        :param url: URL запроса.
        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :return: Модель детальной информации о подменю.
        """
        result_cache: SubmenuDetailModel | None = await self.cache_service.get_cache(url)

        if result_cache:
            return result_cache

        result: SubmenuDetailModel = await self.submenu_repository.get_submenu_detail(menu_id, submenu_id)
        await self.cache_service.set_cache(result, url)

        return await self.submenu_repository.get_submenu_detail(menu_id, submenu_id)

    async def update_submenu(
            self,
            url: str,
            menu_id: UUID,
            submenu_id: UUID,
            submenu_update: SubmenuUpdate
    ) -> SubmenuModel:
        """
        Обновить информацию о подменю.

        :param url: URL запроса.
        :param menu_id: Идентификатор меню, к которому привязано подменю.
        :param submenu_id: Идентификатор подменю, которое нужно обновить.
        :param submenu_update: Схема данных для обновления информации о подменю.
        :return: Модель обновленного подменю.
        """
        result: SubmenuModel = await self.submenu_repository.update_submenu(menu_id, submenu_id, submenu_update)
        await self.cache_service.delete_cache(url, f'get_submenus:{menu_id}')

        return result

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubmenuModel:
        """
        Удалить подменю.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю, которое нужно удалить.
        :return: Модель удаленного подменю
        """
        result: SubmenuModel = await self.submenu_repository.delete_submenu(menu_id, submenu_id)
        await self.cache_service.delete_related_cache('submenu', menu_id=menu_id, submenu_id=submenu_id)

        return result
