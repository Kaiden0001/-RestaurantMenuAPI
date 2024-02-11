from decimal import Decimal
from typing import Any, Union
from uuid import UUID

from src.menu.models.dish_model import DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.submenu_model import SubmenuModel


def is_valid_uuid(uuid_str: str) -> bool:
    """
    Проверяет, является ли переданная строка допустимым UUID.

    :param uuid_str: Строка, предположительно содержащая UUID.
    :return: True, если строка содержит допустимый UUID, в противном случае False.
    """
    try:
        uuid_obj: UUID = UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False
    except AttributeError:
        return False


def is_valid_data(model: str, data: list) -> bool:
    """
    Проверяет корректность данных модели.

    :param model: Тип модели (menu, submenu или dish).
    :param data: Список данных модели.
    :return: True, если данные корректны, в противном случае False.
    """
    if model == 'menu':
        expected_types_menu: list[Any] = [UUID, str, str]
        for index, item in enumerate(data):
            if item == '' or not isinstance(item, expected_types_menu[index]):
                return False
        return True
    elif model == 'submenu':
        expected_types_submenu: list[Any] = [UUID, str, str, UUID]
        for index, item in enumerate(data):
            if item == '' or not isinstance(item, expected_types_submenu[index]):
                return False
        return True
    elif model == 'dish':
        expected_types_dish: list[Any] = [UUID, str, str, Union[Decimal, int, float], UUID]
        try:
            data[3] = Decimal(data[3])
        except Exception:
            return False
        for index, item in enumerate(data):
            if item == '' or not isinstance(item, expected_types_dish[index]):
                return False
        return True
    return False


def parse_sheet(values: list) -> tuple[list[MenuModel], list[SubmenuModel], list[DishModel | Any]]:
    """
    Разбирает данные листа и создает объекты моделей меню, подменю и блюд.

    :param values: Список списков значений листа.
    :return: Кортеж из списков моделей меню, подменю и блюд.
    """
    menu_data: list[MenuModel] = []
    submenu_data: list[SubmenuModel] = []
    dish_data: list[DishModel | Any] = []

    menu_id: UUID | None = None
    submenu_id: UUID | None = None

    if [[]] == values:
        return menu_data, submenu_data, dish_data

    for value in values:
        if value[0]:
            menu_id, submenu_id = None, None
            if is_valid_uuid(value[0]):
                check_data: bool = is_valid_data(
                    'menu',
                    [UUID(value[0]), value[1], value[2]]
                )
                if check_data:
                    menu_id = UUID(value[0])
                    menu_data.append(
                        MenuModel(
                            id=menu_id,
                            title=value[1],
                            description=value[2]
                        )
                    )
                    continue
                else:
                    continue
        elif value[1]:
            submenu_id = None
            if is_valid_uuid(value[1]):
                if menu_id is not None:
                    check_data = is_valid_data(
                        'submenu',
                        [UUID(value[1]), value[2], value[3], menu_id]
                    )
                    if check_data:
                        submenu_id = UUID(value[1])
                        submenu_data.append(
                            SubmenuModel(
                                id=submenu_id,
                                title=value[2],
                                description=value[3],
                                menu_id=menu_id
                            )
                        )
                        continue
                continue
        elif value[2]:
            if is_valid_uuid(value[2]):
                if submenu_id is not None:
                    check_data = is_valid_data(
                        'dish',
                        [UUID(value[2]), value[3], value[4], value[5], submenu_id]
                    )
                    if check_data:
                        try:
                            if value[6] and 100 >= int(value[6]) >= 0:
                                discount: Decimal = Decimal(value[5]) * (Decimal(value[6]) / 100)
                                value[5] = round(Decimal(value[5]) - discount, 2)
                        except Exception:
                            pass
                        price = value[5]
                        dish_data.append(
                            [
                                DishModel(
                                    id=UUID(value[2]),
                                    title=value[3],
                                    description=value[4],
                                    price=price,
                                    submenu_id=submenu_id
                                ),
                                menu_id
                            ]
                        )
    return menu_data, submenu_data, dish_data
