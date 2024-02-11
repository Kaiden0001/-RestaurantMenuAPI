import json
from typing import Any

import httpx

from src.menu.models.dish_model import DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.submenu_model import SubmenuModel
from src.menu.tests.utils import reverse

BASE_URL: str = 'http://web:8000'


def check_menu_data(menu_data_online: list[MenuModel], menu_data_offline: list[MenuModel]) -> None:
    """
    Проверяет данные меню, сравнивая данные онлайн и оффлайн.
    Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

    :param menu_data_online: Список моделей данных меню онлайн.
    :param menu_data_offline: Список моделей данных меню оффлайн.
    """
    for offline_menu in menu_data_offline:
        found: bool = False
        for online_menu in menu_data_online:
            if offline_menu.id == online_menu.id:
                found = True
                if offline_menu != online_menu:
                    httpx.patch(
                        BASE_URL + reverse('update_menu', offline_menu.id),
                        json=json.loads(offline_menu.model_dump_json())
                    )
                break
        if not found:
            httpx.post(
                BASE_URL + reverse('create_menu'),
                json=json.loads(offline_menu.model_dump_json())
            )


def check_submenu_data(submenu_data_online: list[SubmenuModel], submenu_data_offline: list[SubmenuModel]) -> None:
    """
    Проверяет данные подменю, сравнивая данные онлайн и оффлайн.
    Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

    :param submenu_data_online: Список моделей данных подменю онлайн.
    :param submenu_data_offline: Список моделей данных подменю оффлайн.
    """
    for offline_submenu in submenu_data_offline:
        found: bool = False
        for online_submenu in submenu_data_online:
            if offline_submenu.id == online_submenu.id:
                found = True
                if offline_submenu != online_submenu:
                    httpx.patch(
                        BASE_URL + reverse('update_submenu', offline_submenu.menu_id, offline_submenu.id),
                        json=json.loads(offline_submenu.model_dump_json())
                    )
                break
        if not found:
            httpx.post(
                BASE_URL + reverse('create_submenu', offline_submenu.menu_id),
                json=json.loads(offline_submenu.model_dump_json())
            )


def check_dish_data(dish_data_online: list[DishModel], dish_data_offline: list[DishModel | Any]) -> None:
    """
    Проверяет данные блюд, сравнивая данные онлайн и оффлайн.
    Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

    :param dish_data_online: Список моделей данных блюд онлайн.
    :param dish_data_offline: Список моделей данных блюд оффлайн.
    """
    for offline_dish in dish_data_offline:
        found: bool = False
        for online_dish in dish_data_online:
            if offline_dish[0].id == online_dish[0].id:
                found = True
                if offline_dish[0] != online_dish[0]:
                    httpx.patch(
                        BASE_URL + reverse(
                            'update_dish',
                            offline_dish[1],
                            offline_dish[0].submenu_id,
                            offline_dish[0].id
                        ),
                        json=json.loads(offline_dish[0].model_dump_json())
                    )
                break
        if not found:
            httpx.post(
                BASE_URL + reverse(
                    'create_dish',
                    offline_dish[1],
                    offline_dish[0].submenu_id
                ),
                json=json.loads(offline_dish[0].model_dump_json())
            )


def delete_dishes(dish_data_online: list[DishModel], dish_data_offline: list[DishModel | Any]) -> None:
    """
    Удаляет блюда, которых нет в списке оффлайн данных.

    :param dish_data_online: Список моделей данных блюд онлайн.
    :param dish_data_offline: Список моделей данных блюд оффлайн.
    """
    online_dish_ids: list[tuple] = [(dish[0].id, dish[0].submenu_id, dish[1]) for dish in dish_data_online]
    offline_dish_ids: list[tuple] = [(dish[0].id, dish[0].submenu_id, str(dish[1])) for dish in dish_data_offline]
    dishes_to_delete_ids: list[tuple] = [dish for dish in online_dish_ids if dish not in offline_dish_ids]

    for dish in dishes_to_delete_ids:
        httpx.delete(BASE_URL + reverse('delete_dish', dish[2], dish[1], dish[0]))


def delete_submenus(submenu_data_online: list[SubmenuModel], submenu_data_offline: list[SubmenuModel]) -> None:
    """
    Удаляет подменю, которых нет в списке оффлайн данных.

    :param submenu_data_online: Список моделей данных подменю онлайн.
    :param submenu_data_offline: Список моделей данных подменю оффлайн.
    """
    online_submenu_ids: list[tuple] = [(submenu.id, submenu.menu_id) for submenu in submenu_data_online]
    offline_submenu_ids: list[tuple] = [(submenu.id, submenu.menu_id) for submenu in submenu_data_offline]
    submenus_to_delete_ids: list[tuple] = [
        submenu for submenu in online_submenu_ids if submenu not in offline_submenu_ids
    ]
    for submenu in submenus_to_delete_ids:
        httpx.delete(BASE_URL + reverse('delete_submenu', submenu[1], submenu[0]))


def delete_menus(menu_data_online: list[MenuModel], menu_data_offline: list[MenuModel]) -> None:
    """
    Удаляет меню, которых нет в списке оффлайн данных.

    :param menu_data_online: Список моделей данных меню онлайн.
    :param menu_data_offline: Список моделей данных меню оффлайн.
    """
    online_menu_ids: list[str] = [menu.id for menu in menu_data_online]
    offline_menu_ids: list[str] = [menu.id for menu in menu_data_offline]
    menus_to_delete_ids: list[str] = [menu_id for menu_id in online_menu_ids if menu_id not in offline_menu_ids]

    for menu_id in menus_to_delete_ids:
        httpx.delete(BASE_URL + reverse('delete_menu', menu_id))
