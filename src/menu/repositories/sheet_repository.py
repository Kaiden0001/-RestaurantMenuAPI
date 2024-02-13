import json
from decimal import Decimal
from typing import Any, Union
from uuid import UUID

import gspread
from gspread import Client, Spreadsheet
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import BASE_DIR, SPREADSHEET_URL
from src.menu.models.dish_model import DishDiscountModel, DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.models_for_full_menu import AllMenuModel, MenuInfo
from src.menu.models.submenu_model import SubmenuModel
from src.menu.repositories.dish_repository import DishRepository
from src.menu.repositories.menu_repository import MenuRepository
from src.menu.repositories.submenu_repository import SubmenuRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate


class SheetRepository:

    def __init__(self, session: AsyncSession):
        self.menu_repository: MenuRepository = MenuRepository(session)
        self.submenu_repository: SubmenuRepository = SubmenuRepository(session)
        self.dish_repository: DishRepository = DishRepository(session)

    @staticmethod
    def _is_valid_uuid(uuid_str: str) -> bool:
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

    @staticmethod
    def _is_valid_data(model: str, data: list) -> bool:
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

    @staticmethod
    def _get_values() -> list[list]:
        """
        Получает данные из Google Sheets.

        :return: Список списков значений из листа таблицы.
        """
        try:
            client: Client = gspread.service_account(BASE_DIR / 'service_account.json')
            sh: Spreadsheet = client.open_by_url(SPREADSHEET_URL)
            values: list[list] = sh.sheet1.get_all_values()
            return values
        except Exception:
            print('Data retrieval error')
            return [[]]

    def parse_sheet(self) -> tuple[list[MenuModel], list[SubmenuModel], list[DishDiscountModel | Any]]:
        """
            Разбирает данные листа и создает объекты моделей меню, подменю и блюд.

            :param values: Список списков значений листа.
            :return: Кортеж из списков моделей меню, подменю и блюд.
        """
        menu_data: list[MenuModel] = []
        submenu_data: list[SubmenuModel] = []
        dish_data: list[DishDiscountModel | Any] = []
        values: list[list] = self._get_values()

        menu_id: UUID | None = None
        submenu_id: UUID | None = None

        if [[]] == values:
            return menu_data, submenu_data, dish_data

        for value in values:
            if value[0]:
                menu_id, submenu_id = None, None
                if self._is_valid_uuid(value[0]):
                    check_data: bool = self._is_valid_data(
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
                if self._is_valid_uuid(value[1]):
                    if menu_id is not None:
                        check_data = self._is_valid_data(
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
                if self._is_valid_uuid(value[2]):
                    if submenu_id is not None:
                        check_data = self._is_valid_data(
                            'dish',
                            [UUID(value[2]), value[3], value[4], value[5], submenu_id]
                        )
                        if check_data:
                            discount_value: Any = None
                            try:
                                if value[6] and 100 >= int(value[6]) >= 0:
                                    discount: Decimal = Decimal(value[5]) * (Decimal(value[6]) / 100)
                                    discount_value = round(Decimal(value[5]) - discount, 2)
                                    if value[6] == 100 or value[6] == 0:
                                        discount_value = None
                            except Exception:
                                pass
                            price = value[5]
                            dish_data.append(
                                [
                                    DishDiscountModel(
                                        id=UUID(value[2]),
                                        title=value[3],
                                        description=value[4],
                                        price=price,
                                        submenu_id=submenu_id,
                                        discount=discount_value
                                    ),
                                    menu_id,
                                    discount_value
                                ]
                            )
        return menu_data, submenu_data, dish_data

    async def get_full_menu(self) -> tuple[list[MenuModel], list[SubmenuModel], list[DishModel | Any]]:
        """
        Получает полное меню из удалённого источника данных.

        :return: Кортеж, содержащий списки моделей меню, подменю и блюд.
        """
        menu_data: list[MenuModel] = []
        submenu_data: list[SubmenuModel] = []
        dish_data: list[DishModel | Any] = []

        full_menu: list[AllMenuModel] = await self.menu_repository.get_full_menu()

        for data in full_menu:
            menu: MenuInfo = data.menu
            menu_data.append(
                MenuModel(
                    id=menu.id,
                    title=menu.title,
                    description=menu.description,
                )
            )
            for submenu in menu.submenus:
                submenu_data.append(
                    SubmenuModel(
                        id=submenu.id,
                        title=submenu.title,
                        description=submenu.description,
                        menu_id=menu.id
                    )
                )
                for dish in submenu.dishes:
                    dish_data.append(
                        [
                            DishModel(
                                id=dish.id,
                                title=dish.title,
                                description=dish.description,
                                price=dish.price,
                                submenu_id=submenu.id
                            ),
                            menu.id
                        ]
                    )

        return menu_data, submenu_data, dish_data

    async def delete_dishes(
            self,
            dish_data_online: list[DishModel],
            dish_data_offline: list[DishModel | Any]
    ) -> list[tuple]:
        """
        Удаляет блюда, которых нет в списке оффлайн данных.

        :param dish_data_online: Список моделей данных блюд онлайн.
        :param dish_data_offline: Список моделей данных блюд оффлайн.
        """
        online_dish_ids: list[tuple] = [(dish[0].id, dish[0].submenu_id, dish[1]) for dish in dish_data_online]
        offline_dish_ids: list[tuple] = [(dish[0].id, dish[0].submenu_id, dish[1]) for dish in dish_data_offline]
        dishes_to_delete_ids: list[tuple] = [dish for dish in online_dish_ids if dish not in offline_dish_ids]

        for dish in dishes_to_delete_ids:
            await self.dish_repository.delete_dish(str(dish[0]))

        return dishes_to_delete_ids

    async def delete_submenus(
            self,
            submenu_data_online: list[SubmenuModel],
            submenu_data_offline: list[SubmenuModel]
    ) -> list[tuple]:
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
            await self.submenu_repository.delete_submenu(submenu[1], submenu[0])

        return submenus_to_delete_ids

    async def delete_menus(self, menu_data_online: list[MenuModel], menu_data_offline: list[MenuModel]) -> list[str]:
        """
        Удаляет меню, которых нет в списке оффлайн данных.

        :param menu_data_online: Список моделей данных меню онлайн.
        :param menu_data_offline: Список моделей данных меню оффлайн.
        """
        online_menu_ids: list[str] = [menu.id for menu in menu_data_online]
        offline_menu_ids: list[str] = [menu.id for menu in menu_data_offline]
        menus_to_delete_ids: list[str] = [menu_id for menu_id in online_menu_ids if menu_id not in offline_menu_ids]

        for menu_id in menus_to_delete_ids:
            await self.menu_repository.delete_menu(menu_id)

        return menus_to_delete_ids

    @staticmethod
    async def get_update_or_create_menu(
            menu_data_online: list[MenuModel],
            menu_data_offline: list[MenuModel]
    ) -> tuple[list, list]:
        """
        Проверяет данные меню, сравнивая данные онлайн и оффлайн.
        Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

        :param menu_data_online: Список моделей данных меню онлайн.
        :param menu_data_offline: Список моделей данных меню оффлайн.
        """
        menus_create: list = []
        menus_update: list = []

        for offline_menu in menu_data_offline:
            found: bool = False
            for online_menu in menu_data_online:
                if offline_menu.id == online_menu.id:
                    found = True
                    if offline_menu != online_menu:
                        menus_update.append(
                            [offline_menu.id, MenuUpdate(**json.loads(offline_menu.model_dump_json()))]
                        )
                    break
            if not found:
                menus_create.append(
                    MenuCreate(**json.loads(offline_menu.model_dump_json()))
                )
        return menus_update, menus_create

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> None:
        await self.menu_repository.update_menu(menu_id, menu_update)

    async def create_menu(self, menu_create: MenuCreate) -> None:
        await self.menu_repository.create_menu(menu_create)

    @staticmethod
    async def get_update_or_create_submenu(
            submenu_data_online: list[SubmenuModel],
            submenu_data_offline: list[SubmenuModel]
    ) -> tuple[list, list]:
        """
        Проверяет данные подменю, сравнивая данные онлайн и оффлайн.
        Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

        :param submenu_data_online: Список моделей данных подменю онлайн.
        :param submenu_data_offline: Список моделей данных подменю оффлайн.
        """
        submenus_create: list = []
        submenus_update: list = []

        for offline_submenu in submenu_data_offline:
            found: bool = False
            for online_submenu in submenu_data_online:
                if offline_submenu.id == online_submenu.id:
                    found = True
                    if offline_submenu != online_submenu:
                        submenus_update.append(
                            [
                                offline_submenu.menu_id,
                                offline_submenu.id,
                                SubmenuUpdate(**json.loads(offline_submenu.model_dump_json()))
                            ]
                        )
                    break
            if not found:
                submenus_create.append(
                    [
                        offline_submenu.menu_id,
                        SubmenuCreate(**json.loads(offline_submenu.model_dump_json()))
                    ]
                )
        return submenus_update, submenus_create

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate) -> None:
        await self.submenu_repository.update_submenu(menu_id, submenu_id, submenu_update)

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> None:
        await self.submenu_repository.create_submenu(menu_id, submenu_create)

    @staticmethod
    async def get_update_or_create_dish(
            dish_data_online: list[DishModel],
            dish_data_offline: list[DishModel | Any]
    ) -> tuple[list, list]:
        """
        Проверяет данные блюд, сравнивая данные онлайн и оффлайн.
        Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

        :param dish_data_online: Список моделей данных блюд онлайн.
        :param dish_data_offline: Список моделей данных блюд оффлайн.
        """
        dishes_create: list = []
        dishes_update: list = []

        for offline_dish in dish_data_offline:
            found: bool = False
            for online_dish in dish_data_online:
                if offline_dish[0].id == online_dish[0].id:
                    found = True
                    if offline_dish[0].discount == Decimal(0.00):
                        offline_dish[0].discount = None
                    if offline_dish[0] != online_dish[0]:
                        dishes_update.append(
                            [
                                offline_dish[1],
                                offline_dish[0].submenu_id,
                                offline_dish[0].id,
                                DishUpdate(**json.loads(offline_dish[0].model_dump_json())),
                                offline_dish[2]
                            ]
                        )
                    break
            if not found:
                dishes_create.append(
                    [
                        offline_dish[1],
                        offline_dish[0].submenu_id,
                        DishCreate(**json.loads(offline_dish[0].model_dump_json())),
                        offline_dish[2]
                    ]
                )
        return dishes_update, dishes_create

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate) -> None:
        await self.dish_repository.update_dish(dish_id, dish_update)

    async def create_dish(self, submenu_id: UUID, dish_create: DishCreate) -> DishModel:
        return await self.dish_repository.create_dish(submenu_id, dish_create)
