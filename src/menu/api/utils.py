from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.repositories.dish_repository import DishRepository
from src.menu.repositories.menu_repository import MenuRepository
from src.menu.repositories.submenu_repository import SubmenuRepository
from src.menu.services.dish_service import DishService
from src.menu.services.menu_service import MenuService
from src.menu.services.submenu_service import SubmenuService


async def get_menu_service(
        session: AsyncSession = Depends(get_async_session)) -> MenuService:
    """
    Получение сервиса для работы с меню.

    :param session: Асинхронная сессия базы данных.
    :return: Экземпляр сервиса для работы с меню.
    """
    menu_repository: MenuRepository = MenuRepository(session)
    return MenuService(menu_repository)


async def get_submenu_service(
        session: AsyncSession = Depends(get_async_session)) -> SubmenuService:
    """
    Получение сервиса для работы с подменю.

    :param session: Асинхронная сессия базы данных.
    :return: Экземпляр сервиса для работы с подменю.
    """
    submenu_repository: SubmenuRepository = SubmenuRepository(session)
    return SubmenuService(submenu_repository)


async def get_dish_service(
        session: AsyncSession = Depends(get_async_session)) -> DishService:
    """
    Получение сервиса для работы с блюдами.

    :param session: Асинхронная сессия базы данных.
    :return: Экземпляр сервиса для работы с блюдами.
    """
    dish_repository: DishRepository = DishRepository(session)
    return DishService(dish_repository)
