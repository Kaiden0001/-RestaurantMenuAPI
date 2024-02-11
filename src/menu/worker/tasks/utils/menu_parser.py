from typing import Any

import httpx
from httpx import Response

from src.menu.models.dish_model import DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.submenu_model import SubmenuModel
from src.menu.tests.utils import reverse
from src.menu.worker.tasks.utils.check_data import BASE_URL


def get_full_menu() -> tuple[list[MenuModel], list[SubmenuModel], list[DishModel | Any]]:
    """
    Получает полное меню из удалённого источника данных.

    :return: Кортеж, содержащий списки моделей меню, подменю и блюд.
    """
    menu_data: list[MenuModel] = []
    submenu_data: list[SubmenuModel] = []
    dish_data: list[DishModel | Any] = []

    full_menu: Response = httpx.get(BASE_URL + reverse('get_full_menu'))
    full_menu_json: list[dict] = full_menu.json()

    for data in full_menu_json:
        menu: dict = data.get('menu', {})
        menu_data.append(
            MenuModel(
                id=menu.get('id'),
                title=menu.get('title'),
                description=menu.get('description'),
            )
        )
        for submenu in menu.get('submenus', []):
            submenu_data.append(
                SubmenuModel(
                    id=submenu.get('id'),
                    title=submenu.get('title'),
                    description=submenu.get('description'),
                    menu_id=menu.get('id')
                )
            )
            for dish in submenu.get('dishes', []):
                dish_data.append(
                    [
                        DishModel(
                            id=dish.get('id'),
                            title=dish.get('title'),
                            description=dish.get('description'),
                            price=dish.get('price'),
                            submenu_id=submenu.get('id')
                        ),
                        menu.get('id')
                    ]
                )

    return menu_data, submenu_data, dish_data
