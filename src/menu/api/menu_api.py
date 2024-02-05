from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from src.menu.api.dependencies import get_menu_service
from src.menu.models.menu_model import MenuDetailModel, MenuModel
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate
from src.menu.services.menu_service import MenuService

router = APIRouter(
    prefix='/api/v1',
    tags=['Menu']
)


@router.get(
    '/menus',
    response_model=list[MenuModel]
)
async def get_menus(
        menu_service: MenuService = Depends(get_menu_service)
) -> list[MenuModel]:
    """
    Получить список всех меню.

    :param menu_service: Сервис для работы с меню (внедрение зависимости).
    :return: Список моделей меню.
    """
    return await menu_service.get_menus()


@router.post(
    '/menus',
    response_model=MenuModel,
    status_code=status.HTTP_201_CREATED
)
async def create_menu(
        menu_create: MenuCreate,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuModel:
    """
    Создать новое меню.

    :param menu_create: Схема данных для создания меню.
    :param menu_service: Сервис для работы с меню (внедрение зависимости).
    :return: Модель созданного меню.
    """
    return await menu_service.create_menu(menu_create)


@router.get(
    '/menus/{menu_id}',
    response_model=MenuDetailModel
)
async def get_menu(
        request: Request,
        menu_id: UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuDetailModel:
    """
    Получить детали конкретного меню по его идентификатору.

    :param request: Объект запроса.
    :param menu_id: Идентификатор меню.
    :param menu_service: Сервис для работы с меню (внедрение зависимости).
    :return: Модель деталей меню.
    """
    return await menu_service.get_menu(request.url.path, menu_id)


@router.patch(
    '/menus/{menu_id}',
    response_model=MenuModel
)
async def update_menu(
        request: Request,
        menu_id: UUID,
        menu_update: MenuUpdate,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuModel:
    """
    Обновить информацию о меню.

    :param request: Объект запроса.
    :param menu_id: Идентификатор меню, которое нужно обновить.
    :param menu_update: Схема данных для обновления информации о меню.
    :param menu_service: Сервис для работы с меню (внедрение зависимости).
    :return: Модель обновленного меню.
    """
    return await menu_service.update_menu(request.url.path, menu_id, menu_update)


@router.delete(
    '/menus/{menu_id}',
    response_model=MenuModel
)
async def delete_menu(
        menu_id: UUID,
        menu_service: MenuService = Depends(get_menu_service)
) -> MenuModel:
    """
    Удалить меню по его идентификатору.

    :param menu_id: Идентификатор меню, которое нужно удалить.
    :param menu_service: Сервис для работы с меню (внедрение зависимости).
    :return: Модель удаленного меню.
    """
    return await menu_service.delete_menu(menu_id)
