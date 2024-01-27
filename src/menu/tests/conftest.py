import asyncio
import os
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Any, Generator

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture
def menu_data() -> dict:
    return {
        'title': 'Title',
        'description': 'Description'
    }


@pytest.fixture
def menu_update_data() -> dict:
    return {
        'title': 'Title update',
        'description': 'Description update'
    }


@pytest.fixture
def submenu_data() -> dict:
    return {
        'title': 'Title',
        'description': 'Description'
    }


@pytest.fixture
def submenu_update_data() -> dict:
    return {
        'title': 'Title update',
        'description': 'Description update'
    }


@pytest.fixture
def dish_data() -> dict:
    return {
        'title': 'Title',
        'description': 'Description',
        'price': '5.20',
        'submenu_id': 'ebae19d0-8cda-4f55-902b-e3d6a0bd6747'
    }


@pytest.fixture
def dish_update_data() -> dict:
    return {
        'title': 'Title update',
        'description': 'Description update',
        'price': '14.50'
    }


@pytest.fixture
async def menu_id() -> str:
    return os.environ.get('menu_id')


@pytest.fixture
async def submenu_id() -> str:
    return os.environ.get('submenu_id')


@pytest.fixture
async def dish_id() -> str:
    return os.environ.get('dish_id')


@pytest.fixture(scope='session')
def event_loop(request: Any) -> Generator[AbstractEventLoop, Any, None]:
    loop: AbstractEventLoop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://web/api/v1') as client:
        yield client


def set_env_variable(key: str, value: str) -> None:
    os.environ.setdefault(key, value)


def remove_environment_variable(*args) -> None:
    for env_var in args:
        if env_var in os.environ:
            del os.environ[env_var]
