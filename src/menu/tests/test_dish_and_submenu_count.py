from httpx import AsyncClient, Response

from src.menu.tests.conftest import remove_environment_variable, set_env_variable
from src.menu.tests.utils import reverse


async def test_create_menu(client: AsyncClient, menu_data: dict) -> None:
    response: Response = await client.post(reverse('create_menu'), json=menu_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json

    set_env_variable('menu_id', response_json['id'])


async def test_create_submenu(client: AsyncClient, submenu_data: dict, menu_id: str) -> None:
    response: Response = await client.post(reverse('create_submenu', menu_id), json=submenu_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json

    set_env_variable('submenu_id', response_json['id'])


async def test_create_dish_one(client: AsyncClient, dish_data: dict, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.post(reverse('create_dish', menu_id, submenu_id), json=dish_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json


async def test_create_dish_two(client: AsyncClient, dish_update_data: dict, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.post(reverse('create_dish', menu_id, submenu_id), json=dish_update_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json


async def test_get_menu(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.get(reverse('get_menu', menu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['dishes_count'] == 2
    assert response_json['submenus_count'] == 1


async def test_get_submenu(client: AsyncClient, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.get(reverse('get_submenu', menu_id, submenu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['dishes_count'] == 2


async def test_delete_submenu(client: AsyncClient, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.delete(reverse('delete_submenu', menu_id, submenu_id))

    assert response.status_code == 200


async def test_get_submenus(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.get(reverse('get_submenus', menu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 0


async def test_get_dishes(client: AsyncClient, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.get(reverse('get_dishes', menu_id, submenu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 0


async def test_get_menu_two(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.get(reverse('get_menu', menu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['dishes_count'] == 0
    assert response_json['submenus_count'] == 0


async def test_delete_menu(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.delete(reverse('delete_menu', menu_id))

    assert response.status_code == 200


async def test_get_menus(client: AsyncClient) -> None:
    response: Response = await client.get(reverse('get_menus'))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 0

    remove_environment_variable('menu_id', 'submenu_id', 'dish_id')
