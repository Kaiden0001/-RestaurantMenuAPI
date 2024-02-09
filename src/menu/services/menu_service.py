from uuid import UUID

from aioredis import Redis
from fastapi import BackgroundTasks

from src.menu.models.menu_model import MenuDetailModel, MenuModel
from src.menu.models.models_for_full_menu import AllMenuModel
from src.menu.repositories.menu_repository import MenuRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate
from src.menu.services.cache_service import CacheService


class MenuService:
    def __init__(self, menu_repository: MenuRepository, redis: Redis, background_tasks: BackgroundTasks):
        self.menu_repository = menu_repository
        self.cache_service: CacheService = CacheService(redis)
        self.background_tasks: BackgroundTasks = background_tasks

    async def get_menus(self) -> list[MenuDetailModel]:
        """
        Получить список меню.

        :return: Список моделей меню.
        """
        result_cache: list[MenuDetailModel] | None = await self.cache_service.get_cache('get_menus')
        if result_cache:
            return result_cache

        result: list[MenuDetailModel] = await self.menu_repository.get_menus()

        await self.cache_service.set_cache(cache_key='get_menus', result=result)
        return result

    async def get_full_menu(self) -> list[AllMenuModel]:
        """
        Получение полного меню вместе со всеми подменю и блюдами.

        :return: Список моделей данных AllMenuModel.
        """
        result_cache: list[AllMenuModel] | None = await self.cache_service.get_cache('get_full_menu')
        if result_cache:
            return result_cache

        result = await self.menu_repository.get_full_menu()

        await self.cache_service.set_cache(cache_key='get_full_menu', result=result)
        return result

    async def create_menu(self, menu_create: MenuCreate) -> MenuModel:
        """
        Создать новое меню.

        :param menu_create: Данные для создания меню.
        :return: Модель созданного меню.
        """
        self.background_tasks.add_task(self.cache_service.delete_cache, 'get_menus')
        return await self.menu_repository.create_menu(menu_create)

    async def get_menu(self, url: str, menu_id: UUID) -> MenuDetailModel:
        """
        Получить детальную информацию о меню.

        :param url: URL запроса.
        :param menu_id: Идентификатор меню.
        :return: Модель детальной информации о меню.
        """
        result_cache: MenuDetailModel | None = await self.cache_service.get_cache(url)

        if result_cache:
            return result_cache

        result: MenuDetailModel = await self.menu_repository.get_menu_detail(menu_id)
        await self.cache_service.set_cache(cache_key=url, result=result)

        return result

    async def update_menu(self, url: str, menu_id: UUID, menu_update: MenuUpdate) -> MenuModel:
        """
        Обновить информацию о меню.

        :param url: URL запроса.
        :param menu_id: Идентификатор меню, которое нужно обновить.
        :param menu_update: Схема данных для обновления информации о меню.
        :return: Модель обновленного меню.
        """
        self.background_tasks.add_task(self.cache_service.delete_cache, 'get_menus', url)
        return await self.menu_repository.update_menu(menu_id, menu_update)

    async def delete_menu(self, menu_id: UUID) -> MenuModel:
        """
        Удалить меню.

        :param menu_id: Идентификатор меню, которое нужно удалить.
        :return: Модель удаленного меню.
        """
        self.background_tasks.add_task(self.cache_service.delete_related_cache, service='menu', menu_id=menu_id)
        return await self.menu_repository.delete_menu(menu_id)
