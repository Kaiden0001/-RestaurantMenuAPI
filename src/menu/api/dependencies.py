from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session, get_redis
from src.menu.repositories.dish_repository import DishRepository
from src.menu.repositories.menu_repository import MenuRepository
from src.menu.repositories.submenu_repository import SubmenuRepository
from src.menu.services.dish_service import DishService
from src.menu.services.menu_service import MenuService
from src.menu.services.submenu_service import SubmenuService


async def get_menu_service(
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
) -> MenuService:
    """
    Получение сервиса для работы с меню.

    :param session: Асинхронная сессия базы данных.
    :param redis: Объект Redis.
    :return: Экземпляр сервиса для работы с меню.
    """
    menu_repository: MenuRepository = MenuRepository(session)
    return MenuService(menu_repository, redis)


async def get_submenu_service(
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
) -> SubmenuService:
    """
    Получение сервиса для работы с подменю.

    :param session: Асинхронная сессия базы данных.
    :param redis: Объект Redis.
    :return: Экземпляр сервиса для работы с подменю.
    """
    submenu_repository: SubmenuRepository = SubmenuRepository(session)
    return SubmenuService(submenu_repository, redis)


async def get_dish_service(
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
) -> DishService:
    """
    Получение сервиса для работы с блюдами.

    :param session: Асинхронная сессия базы данных.
    :param redis: Объект Redis.
    :return: Экземпляр сервиса для работы с блюдами.
    """
    dish_repository: DishRepository = DishRepository(session)
    return DishService(dish_repository, redis)
