from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from src.menu.api.dependencies import get_dish_service
from src.menu.models.dish_model import DishModel
from src.menu.schemas.dish_schema import DishCreate, DishUpdate
from src.menu.services.dish_service import DishService

router = APIRouter(
    prefix='/api/v1',
    tags=['Dish']
)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[DishModel])
async def get_dishes(
        menu_id: UUID,
        submenu_id: UUID,
        dish_service: DishService = Depends(get_dish_service)
) -> list[DishModel]:
    """
    Получить список блюд для указанного подменю.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_service: Сервис для работы с блюдами (внедрение зависимости).
    :return: Список моделей блюд.
    """
    return await dish_service.get_dishes(menu_id, submenu_id)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishModel
)
async def get_dish(
        request: Request,
        dish_id: UUID,
        dish_service: DishService = Depends(get_dish_service)
) -> DishModel:
    """
    Получить информацию о конкретном блюде по его идентификатору.

    :param request: Объект запроса.
    :param dish_id: Идентификатор блюда.
    :param dish_service: Сервис для работы с блюдами (внедрение зависимости).
    :return: Модель блюда.
    """
    return await dish_service.get_dish(request.url.path, dish_id)


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=DishModel,
    status_code=status.HTTP_201_CREATED
)
async def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_create: DishCreate,
        dish_service: DishService = Depends(get_dish_service)
) -> DishModel:
    """
    Создать новое блюдо для указанного подменю.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю, для которого создается блюдо.
    :param dish_create: Схема данных для создания блюда.
    :param dish_service: Сервис для работы с блюдами (внедрение зависимости).
    :return: Модель созданного блюда.
    """
    return await dish_service.create_dish(menu_id, submenu_id, dish_create)


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishModel
)
async def update_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_update: DishUpdate,
        dish_service: DishService = Depends(get_dish_service)
) -> DishModel:
    """
    Обновить информацию о блюде.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда, которое нужно обновить.
    :param dish_update: Схема данных для обновления информации о блюде.
    :param dish_service: Сервис для работы с блюдами (внедрение зависимости).
    :return: Модель обновленного блюда.
    """
    return await dish_service.update_dish(menu_id, submenu_id, dish_id, dish_update)


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishModel
)
async def delete_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish_service: DishService = Depends(get_dish_service)
) -> DishModel:
    """
    Удалить блюдо по его идентификатору.

    :param menu_id: Идентификатор меню.
    :param submenu_id: Идентификатор подменю.
    :param dish_id: Идентификатор блюда, которое нужно удалить.
    :param dish_service: Сервис для работы с блюдами (внедрение зависимости).
    :return: Модель удаленного блюда.
    """
    return await dish_service.delete_dish(menu_id, submenu_id, dish_id)
