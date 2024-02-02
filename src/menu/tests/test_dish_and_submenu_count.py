from httpx import AsyncClient, Response

from src.menu.tests.conftest import remove_environment_variable, set_env_variable


async def test_create_menu(client: AsyncClient,
                           menu_data: dict) -> None:
    response: Response = await client.post('/menus', json=menu_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json

    set_env_variable('menu_id', response_json['id'])


async def test_create_submenu(client: AsyncClient,
                              submenu_data: dict,
                              menu_id: str) -> None:
    response: Response = await client.post(
        f'/menus/{menu_id}/submenus', json=submenu_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json

    set_env_variable('submenu_id', response_json['id'])


async def test_create_dish_one(client: AsyncClient,
                               dish_data: dict,
                               menu_id: str,
                               submenu_id: str) -> None:
    response: Response = await client.post(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json


async def test_create_dish_two(client: AsyncClient,
                               dish_update_data: dict,
                               menu_id: str,
                               submenu_id: str) -> None:
    response: Response = await client.post(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json=dish_update_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json


async def test_get_menu(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.get(f'/menus/{menu_id}')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['dishes_count'] == 2
    assert response_json['submenus_count'] == 1


async def test_get_submenu(client: AsyncClient,
                           menu_id: str,
                           submenu_id: str) -> None:
    response: Response = await client.get(
        f'/menus/{menu_id}/submenus/{submenu_id}')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['dishes_count'] == 2


async def test_delete_submenu(client: AsyncClient,
                              menu_id: str,
                              submenu_id: str) -> None:
    response: Response = await client.delete(
        f'/menus/{menu_id}/submenus/{submenu_id}')

    assert response.status_code == 200


async def test_get_submenus(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.get(f'/menus/{menu_id}/submenus')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 0


async def test_get_dishes(client: AsyncClient,
                          menu_id: str,
                          submenu_id: str) -> None:
    response: Response = await client.get(
        f'/menus/{menu_id}/submenus/{submenu_id}/dishes')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 0


async def test_get_menu_two(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.get(f'/menus/{menu_id}')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['dishes_count'] == 0
    assert response_json['submenus_count'] == 0


async def test_delete_menu(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.delete(f'/menus/{menu_id}')

    assert response.status_code == 200


async def test_get_menus(client: AsyncClient) -> None:
    response: Response = await client.get('/menus')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 0

    remove_environment_variable('menu_id', 'submenu_id', 'dish_id')
