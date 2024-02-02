import uuid

from httpx import AsyncClient, Response

from src.menu.tests.conftest import remove_environment_variable, set_env_variable


async def test_create_submenu(client: AsyncClient,
                              menu_data: dict,
                              submenu_data: dict) -> None:
    menu_response: Response = await client.post('/menus', json=menu_data)
    menu_response_json: dict = menu_response.json()

    submenu_data['menu_id'] = menu_response_json['id']
    response: Response = await client.post(
        f'/menus/{menu_response_json["id"]}/submenus', json=submenu_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']
    assert response_json['menu_id'] == submenu_data['menu_id']

    set_env_variable('menu_id', menu_response_json['id'])
    set_env_variable('submenu_id', response_json['id'])


async def test_get_submenus(client: AsyncClient,
                            submenu_data: dict,
                            menu_id: str) -> None:
    response: Response = await client.get(f'/menus/{menu_id}/submenus')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert 'id' in response_json[0]
    assert response_json[0]['title'] == submenu_data['title']
    assert response_json[0]['description'] == submenu_data['description']
    assert response_json[0]['menu_id'] == menu_id


async def test_get_submenu_detail(client: AsyncClient,
                                  submenu_data: dict,
                                  menu_id: str,
                                  submenu_id: str) -> None:
    response: Response = await client.get(
        f'/menus/{menu_id}/submenus/{submenu_id}')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']
    assert response_json['dishes_count'] == 0


async def test_get_submenu_invalid_id(client: AsyncClient,
                                      submenu_data: dict,
                                      menu_id: str) -> None:
    response: Response = await client.get(
        f'/menus/{menu_id}/submenus/{uuid.uuid4()}')

    assert response.status_code == 404


async def test_patch_submenu(client: AsyncClient,
                             submenu_update_data: dict,
                             menu_id: str,
                             submenu_id: str) -> None:
    response: Response = await client.patch(
        f'/menus/{menu_id}/submenus/{submenu_id}', json=submenu_update_data)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['title'] == submenu_update_data['title']
    assert response_json['description'] == submenu_update_data['description']


async def test_patch_submenu_invalid_id(client: AsyncClient,
                                        submenu_update_data: dict,
                                        menu_id: str) -> None:
    response: Response = await client.patch(
        f'/menus/{menu_id}/submenus/{uuid.uuid4()}', json=submenu_update_data)

    assert response.status_code == 404


async def test_delete_submenu_invalid_id(client: AsyncClient,
                                         menu_id: str) -> None:
    response: Response = await client.delete(
        f'/menus/{menu_id}/{uuid.uuid4()}')

    assert response.status_code == 404


async def test_delete_submenu(client: AsyncClient,
                              menu_id: str,
                              submenu_id: str) -> None:
    response_submenu: Response = await client.delete(
        f'/menus/{menu_id}/submenus/{submenu_id}')
    response_menu: Response = await client.delete(f'/menus/{menu_id}')

    assert response_menu.status_code == 200
    assert response_submenu.status_code == 200

    remove_environment_variable('menu_id', 'submenu_id')
