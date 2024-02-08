import asyncio
import os
from asyncio import AbstractEventLoop
from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture
def menu_data() -> dict[str, str]:
    """
    Фикстура предоставляет образец данных для меню в виде словаря.

    :return: Образец данных меню.
    """
    return {
        'title': 'Title',
        'description': 'Description'
    }


@pytest.fixture
def menu_update_data() -> dict[str, str]:
    """
    Фикстура предоставляет образец данных для обновления меню в виде словаря.

    :return: Образец данных для обновления меню.
    """
    return {
        'title': 'Title update',
        'description': 'Description update'
    }


@pytest.fixture
def submenu_data() -> dict[str, str]:
    """
    Фикстура предоставляет образец данных для подменю в виде словаря.

    :return: Образец данных подменю.
    """
    return {
        'title': 'Title',
        'description': 'Description'
    }


@pytest.fixture
def submenu_update_data() -> dict[str, str]:
    """
    Фикстура предоставляет образец данных для обновления подменю в виде словаря.

    :return: Образец данных для обновления подменю.
    """
    return {
        'title': 'Title update',
        'description': 'Description update'
    }


@pytest.fixture
def dish_data() -> dict[str, str]:
    """
    Фикстура предоставляет образец данных для блюда в виде словаря.

    :return: Образец данных блюда.
    """
    return {
        'title': 'Title',
        'description': 'Description',
        'price': '5.20'
    }


@pytest.fixture
def dish_update_data() -> dict[str, str]:
    """
    Фикстура предоставляет образец данных для обновления блюда в виде словаря.

    :return: Образец данных для обновления блюда.
    """
    return {
        'title': 'Title update',
        'description': 'Description update',
        'price': '14.50'
    }


@pytest.fixture
async def menu_id() -> str | None:
    """
    Фикстура предоставляет идентификатор меню, полученный из переменной
    окружения 'menu_id'.

    :return: Идентификатор меню или None, если не установлен.
    """
    return os.environ.get('menu_id')


@pytest.fixture
async def submenu_id() -> str | None:
    """
    Фикстура предоставляет идентификатор подменю, полученный из переменной
    окружения 'submenu_id'.

    :return: Идентификатор подменю или None, если не установлен.
    """
    return os.environ.get('submenu_id')


@pytest.fixture
async def dish_id() -> str | None:
    """
    Фикстура предоставляет идентификатор блюда, полученный из переменной
    окружения 'dish_id'.

    :return: Идентификатор блюда или None, если не установлен.
    """
    return os.environ.get('dish_id')


@pytest.fixture(scope='session')
def event_loop(request: Any) -> Generator[AbstractEventLoop, Any, None]:
    """
    Фикстура предоставляет сессионный event loop.

    :param request: Объект запроса Pytest.

    :return: Генератор event loop.
    :rtype: Generator[AbstractEventLoop, Any, None]
    """
    loop: AbstractEventLoop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Фикстура предоставляет асинхронного HTTP-клиента с сессионной областью.

    :return: Генератор асинхронного HTTP-клиента.
    :rtype: AsyncGenerator[AsyncClient, None]
    """
    async with AsyncClient(app=app, base_url='http://web_test') as client:
        yield client


def set_env_variable(key: str, value: str) -> None:
    """
    Функция для установки переменной окружения.

    :param key: Название переменной окружения.
    :param value: Значение для установки переменной окружения.

    :return: None
    """
    os.environ.setdefault(key, value)


def remove_environment_variable(*args) -> None:
    """
    Функция для удаления переменных окружения.

    :param args: Произвольное количество названий переменных окружения для удаления.
    :return: None
    """
    for env_var in args:
        if env_var in os.environ:
            del os.environ[env_var]
