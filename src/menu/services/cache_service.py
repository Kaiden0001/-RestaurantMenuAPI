import pickle
from typing import Any

from aioredis import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_cache(self, cache_key: str) -> Any | None:
        """
        Получить данные из кэша по ключу.

        :param cache_key: Ключ кэша.
        :return: Сериализованные данные или None, если данных нет в кэше.
        """
        cached_result: Any = await self.redis.get(cache_key)

        if cached_result:
            result_data: Any = pickle.loads(cached_result)
        else:
            result_data = None

        return result_data

    async def set_cache(self, result: Any, cache_key: str, expiration: int = 3600) -> None:
        """
        Установить данные в кэш по ключу.

        :param result: Данные для кэширования.
        :param cache_key: Ключ кэша.
        :param expiration: Время жизни кэша в секундах (по умолчанию 1 час).
        """
        serialized_result: bytes = pickle.dumps(result)
        await self.redis.setex(cache_key, expiration, serialized_result)

    async def delete_cache(self, *args) -> None:
        """
        Удалить данные из кэша по ключам.

        :param args: Переменное количество ключей кэша.
        """
        await self.redis.unlink(*args)

    async def delete_related_cache(self, service: str, **kwargs) -> None:
        """
        Удалить связанные сущности из кэша в зависимости от типа сервиса.

        :param service: Тип сервиса ('menu', 'submenu' или 'dish').
        :param kwargs: Параметры для определения сущности (menu_id, submenu_id, dish_id).
        """
        caches_to_delete: list = []
        patterns: list = []
        cache_template: str = ''

        match service:
            case 'menu':
                cache_template = f'/api/v1/menus/{kwargs["menu_id"]}'
                cache_template_get_dishes: str = f'get_dishes:{kwargs["menu_id"]}:*'

                caches_to_delete.extend(
                    [
                        'get_menus',
                        f'get_submenus:{kwargs["menu_id"]}',
                        cache_template
                    ]
                )
                patterns.extend([f'{cache_template}:*', cache_template_get_dishes])
            case 'submenu':
                cache_template = f'/api/v1/menus/{kwargs["menu_id"]}/submenus/{kwargs["submenu_id"]}'

                caches_to_delete.extend(
                    [
                        f'get_submenus:{kwargs["menu_id"]}',
                        f'/api/v1/menus/{kwargs["menu_id"]}',
                        f'get_dishes:{kwargs["menu_id"]}:{kwargs["submenu_id"]}',
                        cache_template
                    ]
                )

                patterns.append(f'{cache_template}:*')
            case 'dish':
                caches_to_delete.extend(
                    [
                        f'/api/v1/menus/{kwargs["menu_id"]}/submenus/{kwargs["submenu_id"]}/dishes/{kwargs["dish_id"]}',
                        f'/api/v1/menus/{kwargs["menu_id"]}',
                        f'/api/v1/menus/{kwargs["menu_id"]}/submenus/{kwargs["submenu_id"]}',
                        f'get_dishes:{kwargs["menu_id"]}:{kwargs["submenu_id"]}'
                    ]
                )

        caches_to_delete.append(cache_template)

        for pattern in patterns:
            result: Any = await self.redis.scan(match=pattern)
            for key in result[1]:
                caches_to_delete.append(key.decode('utf-8'))

        await self.redis.unlink(*caches_to_delete)
