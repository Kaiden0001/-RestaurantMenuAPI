from typing import Any

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish_model import DishDiscountModel, DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.submenu_model import SubmenuModel
from src.menu.repositories.sheet_repository import SheetRepository
from src.menu.services.cache_service import CacheService
from src.menu.tests.utils import reverse


class SheetService:
    def __init__(
            self,
            redis: Redis,
            session: AsyncSession,
    ):
        self.redis: Redis = redis
        self.sheet_repository: SheetRepository = SheetRepository(session)
        self.cache_service: CacheService = CacheService(redis)

    async def check_data(self):
        menu_data_offline, submenu_data_offline, dish_data_offline = self.sheet_repository.parse_sheet()
        menu_data_online, submenu_data_online, dish_data_online = await self.sheet_repository.get_full_menu()

        dish_data_online = await self.add_discount_to_dish_online(dish_data_online)

        await self.delete_dishes(dish_data_online, dish_data_offline)
        await self.delete_submenus(submenu_data_online, submenu_data_offline)
        await self.delete_menus(menu_data_online, menu_data_offline)

        menus_update, menus_create = await self.get_update_or_create_menu(menu_data_online, menu_data_offline)
        await self.update_menu(menus_update)
        await self.create_menu(menus_create)

        submenus_update, submenus_create = await self.get_update_or_create_submenu(
            submenu_data_online,
            submenu_data_offline
        )
        await self.update_submenu(submenus_update)
        await self.create_submenu(submenus_create)

        dish_update, dish_create = await self.get_update_or_create_dish(dish_data_online, dish_data_offline)
        await self.update_dish(dish_update)
        await self.create_dish(dish_create)

    async def delete_dishes(
            self,
            dish_data_online: list[DishModel],
            dish_data_offline: list[DishModel | Any]
    ) -> None:
        """
        Удаляет блюда, которых нет в списке оффлайн данных.

        :param dish_data_online: Список моделей данных блюд онлайн.
        :param dish_data_offline: Список моделей данных блюд оффлайн.
        """
        dishes_to_delete_ids: list[tuple] = await self.sheet_repository.delete_dishes(
            dish_data_online,
            dish_data_offline
        )

        for dish in dishes_to_delete_ids:
            await self.cache_service.delete_related_cache(
                'dish',
                menu_id=dish[2],
                submenu_id=dish[1],
                dish_id=dish[0]
            )

    async def delete_submenus(
            self,
            submenu_data_online: list[SubmenuModel],
            submenu_data_offline: list[SubmenuModel]
    ) -> None:
        """
        Удаляет подменю, которых нет в списке оффлайн данных.

        :param submenu_data_online: Список моделей данных подменю онлайн.
        :param submenu_data_offline: Список моделей данных подменю оффлайн.
        """
        submenus_to_delete: list[tuple] = await self.sheet_repository.delete_submenus(
            submenu_data_online,
            submenu_data_offline
        )

        for submenu in submenus_to_delete:
            await self.cache_service.delete_related_cache(
                'submenu',
                menu_id=submenu[0],
                submenu_id=submenu[1]
            )

    async def delete_menus(self, menu_data_online: list[MenuModel], menu_data_offline: list[MenuModel]) -> None:
        """
        Удаляет меню, которых нет в списке оффлайн данных.

        :param menu_data_online: Список моделей данных меню онлайн.
        :param menu_data_offline: Список моделей данных меню оффлайн.
        """
        menus_to_delete: list[str] = await self.sheet_repository.delete_menus(menu_data_online, menu_data_offline)

        for menu in menus_to_delete:
            await self.cache_service.delete_related_cache(
                'menu',
                menu_id=menu
            )

    async def get_update_or_create_menu(
            self,
            menu_data_online: list[MenuModel],
            menu_data_offline: list[MenuModel]
    ) -> tuple[list, list]:
        """
        Проверяет данные меню, сравнивая данные онлайн и оффлайн.

        :param menu_data_online: Список моделей данных меню онлайн.
        :param menu_data_offline: Список моделей данных меню оффлайн.
        """
        return await self.sheet_repository.get_update_or_create_menu(menu_data_online, menu_data_offline)

    async def update_menu(self, menus_to_update: list) -> None:
        for menu in menus_to_update:
            await self.cache_service.delete_cache('get_menus', reverse('update_menu', menu[0]))
            await self.sheet_repository.update_menu(menu[0], menu[1])

    async def create_menu(self, menus_to_create: list) -> None:
        for menu in menus_to_create:
            await self.cache_service.delete_cache('get_menus')
            await self.sheet_repository.create_menu(menu)

    async def get_update_or_create_submenu(
            self,
            submenu_data_online: list[SubmenuModel],
            submenu_data_offline: list[SubmenuModel]
    ) -> tuple[list, list]:
        """
        Проверяет данные подменю, сравнивая данные онлайн и оффлайн.
        Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

        :param submenu_data_online: Список моделей данных подменю онлайн.
        :param submenu_data_offline: Список моделей данных подменю оффлайн.
        """
        return await self.sheet_repository.get_update_or_create_submenu(submenu_data_online, submenu_data_offline)

    async def update_submenu(self, submenus_to_update: list) -> None:
        for submenu in submenus_to_update:
            await self.cache_service.delete_cache(reverse('update_submenu', submenu[0], submenu[1]))
            await self.sheet_repository.update_submenu(submenu[0], submenu[1], submenu[2])

    async def create_submenu(self, submenus_to_create: list) -> None:
        for submenu in submenus_to_create:
            await self.cache_service.delete_cache(
                reverse('create_submenu', submenu[0]),
                f'get_submenus:{submenu[0]}'
            )
            await self.sheet_repository.create_submenu(submenu[0], submenu[1])

    async def get_update_or_create_dish(
            self,
            dish_data_online: list[DishModel],
            dish_data_offline: list[DishModel | Any]
    ) -> tuple[list, list]:
        """
        Проверяет данные блюд, сравнивая данные онлайн и оффлайн.
        Если обнаружены различия, выполняет соответствующие действия (обновление или создание).

        :param dish_data_online: Список моделей данных блюд онлайн.
        :param dish_data_offline: Список моделей данных блюд оффлайн.
        """
        return await self.sheet_repository.get_update_or_create_dish(dish_data_online, dish_data_offline)

    async def update_dish(self, dishes_to_update: list) -> None:
        for dish in dishes_to_update:
            await self.cache_service.delete_cache(
                reverse('update_dish', dish[0], dish[1], dish[2]),
                f'get_dishes:{dish[0]}:{dish[1]}'
            )
            await self.cache_service.delete_cache(f'dish:{dish[2]}')
            if dish[4]:
                await self.cache_service.set_cache(dish[4], f'dish:{dish[2]}', 99999999)

            await self.sheet_repository.update_dish(dish[2], dish[3])

    async def create_dish(self, dishes_to_create: list) -> None:
        for dish in dishes_to_create:
            await self.cache_service.delete_cache(
                f'/api/v1/menus/{dish[0]}',
                f'/api/v1/menus/{dish[0]}/submenus/{dish[1]}',
                f'get_dishes:{dish[0]}:{dish[1]}',
                f'get_submenus:{dish[0]}',
                'get_menus'
            )
            result: DishModel = await self.sheet_repository.create_dish(dish[1], dish[2])

            await self.cache_service.delete_cache(f'dish:{result.id}')
            if dish[3]:
                await self.cache_service.set_cache(dish[3], f'dish:{result.id}', 99999999)

    async def add_discount_to_dish_online(
            self,
            dish_data_online: list[DishModel | Any]
    ) -> list[DishDiscountModel | Any]:
        result: list[DishDiscountModel | Any] = []

        for dish_data in dish_data_online:
            dish_id: str = str(dish_data[0].id)
            discount: Any | None = await self.cache_service.get_cache(f'dish:{dish_id}')

            if discount == dish_data[0].price:
                discount = None
            result.append(
                [DishDiscountModel(**dish_data[0].model_dump(), discount=discount), dish_data[1]]
            )
        return result
