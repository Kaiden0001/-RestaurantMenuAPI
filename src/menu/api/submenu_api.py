from uuid import UUID

from fastapi import APIRouter, Depends

from src.menu.api.utils import get_submenu_service
from src.menu.models.submenu_model import SubmenuDetailModel, SubmenuModel
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate
from src.menu.services.submenu_service import SubmenuService

router = APIRouter(
    prefix='/api/v1',
    tags=['Submenu']
)


@router.get('/menus/{menu_id}/submenus', response_model=list[SubmenuModel])
async def get_submenus(menu_id: UUID,
                       submenu_service: SubmenuService = Depends(get_submenu_service)) -> list[SubmenuModel] | None:
    """
    Получить список подменю для указанного меню.

    :param menu_id: Идентификатор меню.
    :param submenu_service: Сервис для работы с подменю (внедрение зависимости).
    :return: Список моделей подменю.
    """
    return await submenu_service.get_submenus(menu_id)


@router.get('/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuDetailModel)
async def get_submenu(menu_id: UUID,
                      submenu_id: UUID,
                      submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuDetailModel | None:
    """
    Получить подробную информацию о конкретном подменю.

    :param menu_id: Идентификатор меню, к которому относится подменю.
    :param submenu_id: Идентификатор подменю.
    :param submenu_service: Сервис для работы с подменю (внедрение зависимости).
    :return: Модель подменю с деталями.
    """
    return await submenu_service.get_submenu_detail(menu_id, submenu_id)


@router.post('/menus/{menu_id}/submenus', response_model=SubmenuModel, status_code=201)
async def create_submenu(menu_id: UUID,
                         submenu_create: SubmenuCreate,
                         submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuModel | None:
    """
    Создать новое подменю для указанного меню.

    :param menu_id: Идентификатор меню, к которому привязывается подменю.
    :param submenu_create: Схема данных для создания подменю.
    :param submenu_service: Сервис для работы с подменю (внедрение зависимости).
    :return: Модель созданного подменю.
    """
    return await submenu_service.create_submenu(menu_id, submenu_create)


@router.patch('/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuModel)
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         submenu_update: SubmenuUpdate,
                         submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuModel | None:
    """
    Обновить информацию о подменю.

    :param menu_id: Идентификатор меню, к которому относится подменю.
    :param submenu_id: Идентификатор подменю, которое нужно обновить.
    :param submenu_update: Схема данных для обновления информации о подменю.
    :param submenu_service: Сервис для работы с подменю (внедрение зависимости).
    :return: Модель обновленного подменю.
    """
    return await submenu_service.update_submenu(menu_id, submenu_id, submenu_update)


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuModel | None:
    """
    Удалить подменю по его идентификатору.

    :param menu_id: Идентификатор меню, к которому относится подменю.
    :param submenu_id: Идентификатор подменю, которое нужно удалить.
    :param submenu_service: Сервис для работы с подменю (внедрение зависимости).
    :return: Модель удаленного подменю.
    """
    return await submenu_service.delete_submenu(menu_id, submenu_id)
