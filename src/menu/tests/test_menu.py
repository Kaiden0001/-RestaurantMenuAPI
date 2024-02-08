import uuid

from httpx import AsyncClient, Response

from src.menu.tests.conftest import remove_environment_variable, set_env_variable
from src.menu.tests.utils import reverse


async def test_create_menu(client: AsyncClient, menu_data: dict[str, str]) -> None:
    response: Response = await client.post(reverse('create_menu'), json=menu_data)
    response_json: dict[str, str] = response.json()

    assert response.status_code == 201
    assert 'id' in response_json
    assert response_json['title'] == menu_data['title']
    assert response_json['description'] == menu_data['description']

    set_env_variable('menu_id', response_json['id'])


async def test_get_menus(client: AsyncClient, menu_data: dict[str, str]) -> None:
    response: Response = await client.get(reverse('get_menus'))
    response_json: list[dict[str, str | int]] = response.json()

    assert len(response_json) == 1
    assert 'id' in response_json[0]
    assert response_json[0]['title'] == menu_data['title']
    assert response_json[0]['description'] == menu_data['description']


async def test_get_menu_detail(client: AsyncClient, menu_data: dict[str, str], menu_id: str) -> None:
    response: Response = await client.get(reverse('get_menu', menu_id))
    response_json: dict[str, str | int] = response.json()

    assert 'id' in response_json
    assert response_json['title'] == menu_data['title']
    assert response_json['description'] == menu_data['description']
    assert response_json['submenus_count'] == 0
    assert response_json['dishes_count'] == 0


async def test_get_full_menu(
        client: AsyncClient,
        submenu_data: dict[str, str],
        menu_id: str,
        menu_data: dict[str, str],
        dish_data: dict[str, str]
) -> None:
    response_submenu: Response = await client.post(
        reverse(
            'create_submenu',
            menu_id),
        json=submenu_data
    )
    response_submenu_json: dict[str, str] = response_submenu.json()
    await client.post(
        reverse(
            'create_dish',
            menu_id,
            response_submenu_json['id']
        ), json=dish_data
    )
    response: Response = await client.get(reverse('get_full_menu'))
    response_json: list[dict] = response.json()

    assert response_json[0]['menu']['title'] == menu_data['title']
    assert response_json[0]['menu']['description'] == menu_data['description']

    assert response_json[0]['menu']['submenus'][0]['title'] == submenu_data['title']
    assert response_json[0]['menu']['submenus'][0]['description'] == submenu_data['description']

    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['title'] == dish_data['title']
    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['description'] == dish_data['description']
    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['price'] == dish_data['price']


async def test_get_menu_invalid_id(client: AsyncClient) -> None:
    response: Response = await client.get(reverse('get_menu', uuid.uuid4()))

    assert response.status_code == 404


async def test_patch_menu(client: AsyncClient, menu_update_data: dict[str, str], menu_id: str) -> None:
    response: Response = await client.patch(reverse('update_menu', menu_id), json=menu_update_data)
    response_json: dict[str, str] = response.json()

    assert 'id' in response_json
    assert response_json['title'] == menu_update_data['title']
    assert response_json['description'] == menu_update_data['description']


async def test_patch_menu_invalid_id(client: AsyncClient, menu_update_data: dict[str, str]) -> None:
    response: Response = await client.patch(reverse('update_menu', uuid.uuid4()), json=menu_update_data)

    assert response.status_code == 404


async def test_delete_menu(client: AsyncClient, menu_id: str) -> None:
    response: Response = await client.delete(reverse('delete_menu', menu_id))

    assert response.status_code == 200
    remove_environment_variable('menu_id')
