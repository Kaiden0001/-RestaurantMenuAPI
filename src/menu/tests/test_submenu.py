import uuid

from httpx import AsyncClient, Response

from src.menu.tests.conftest import remove_environment_variable, set_env_variable
from src.menu.tests.utils import reverse


async def test_create_submenu(client: AsyncClient, menu_data: dict, submenu_data: dict) -> None:
    menu_response: Response = await client.post(reverse('create_menu'), json=menu_data)
    menu_response_json: dict = menu_response.json()

    submenu_data['menu_id'] = menu_response_json['id']
    response: Response = await client.post(reverse('create_submenu', menu_response_json['id']), json=submenu_data)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert 'id' in response_json
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']
    assert response_json['menu_id'] == submenu_data['menu_id']

    set_env_variable('menu_id', menu_response_json['id'])
    set_env_variable('submenu_id', response_json['id'])


async def test_get_submenus(client: AsyncClient, submenu_data: dict, menu_id: str) -> None:
    response: Response = await client.get(reverse('get_submenus', menu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert 'id' in response_json[0]
    assert response_json[0]['title'] == submenu_data['title']
    assert response_json[0]['description'] == submenu_data['description']
    assert response_json[0]['menu_id'] == menu_id


async def test_get_submenu_detail(client: AsyncClient, submenu_data: dict, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.get(reverse('get_submenu', menu_id, submenu_id))
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']
    assert response_json['dishes_count'] == 0


async def test_get_submenu_invalid_id(client: AsyncClient, submenu_data: dict, menu_id: str) -> None:
    response: Response = await client.get(reverse('get_submenu', menu_id, uuid.uuid4()))

    assert response.status_code == 404


async def test_patch_submenu(client: AsyncClient, submenu_update_data: dict, menu_id: str, submenu_id: str) -> None:
    response: Response = await client.patch(reverse('update_submenu', menu_id, submenu_id), json=submenu_update_data)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['title'] == submenu_update_data['title']
    assert response_json['description'] == submenu_update_data['description']


async def test_patch_submenu_invalid_id(client: AsyncClient, submenu_update_data: dict, menu_id: str) -> None:
    response: Response = await client.patch(reverse('update_submenu', menu_id, uuid.uuid4()), json=submenu_update_data)

    assert response.status_code == 404


async def test_delete_submenu_invalid_id(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.delete(reverse('delete_submenu', menu_id, uuid.uuid4()))

    assert response.status_code == 404


async def test_delete_submenu(client: AsyncClient, menu_id: str, submenu_id: str) -> None:
    response_submenu: Response = await client.delete(reverse('delete_submenu', menu_id, submenu_id))
    response_menu: Response = await client.delete(reverse('delete_menu', menu_id))

    assert response_menu.status_code == 200
    assert response_submenu.status_code == 200

    remove_environment_variable('menu_id', 'submenu_id')
