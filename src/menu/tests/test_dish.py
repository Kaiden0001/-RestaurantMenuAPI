import uuid

from httpx import AsyncClient, Response

from src.menu.tests.conftest import remove_environment_variable, set_env_variable
from src.menu.tests.utils import reverse


async def test_create_dish(
        client: AsyncClient,
        menu_data: dict[str, str],
        submenu_data: dict[str, str],
        dish_data: dict[str, str]
) -> None:
    menu_response: Response = await client.post(reverse('create_menu'), json=menu_data)
    menu_response_json: dict[str, str] = menu_response.json()

    submenu_response: Response = await client.post(
        reverse(
            'create_submenu',
            menu_response_json['id']),
        json=submenu_data
    )
    submenu_response_json: dict[str, str] = submenu_response.json()

    response: Response = await client.post(
        reverse(
            'create_dish',
            submenu_response_json['menu_id'],
            submenu_response_json['id']),
        json=dish_data
    )
    response_json: dict[str, str | float] = response.json()

    assert response.status_code == 201
    assert 'id' in response_json
    assert response_json['title'] == dish_data['title']
    assert response_json['description'] == dish_data['description']
    assert response_json['submenu_id'] == submenu_response_json['id']

    set_env_variable('menu_id', menu_response_json['id'])
    set_env_variable('submenu_id', submenu_response_json['id'])
    set_env_variable('dish_id', str(response_json['id']))


async def test_get_dishes(
        client: AsyncClient,
        dish_data: dict[str, str],
        menu_id: str,
        submenu_id: str
) -> None:
    response: Response = await client.get(reverse('get_dishes', menu_id, submenu_id))
    response_json: list[dict[str, str | float]] = response.json()

    assert response.status_code == 200
    assert 'id' in response_json[0]
    assert response_json[0]['title'] == dish_data['title']
    assert response_json[0]['description'] == dish_data['description']
    assert response_json[0]['submenu_id'] == submenu_id


async def test_get_dish(
        client: AsyncClient,
        submenu_data: dict[str, str],
        menu_id: str,
        submenu_id: str,
        dish_id: str
) -> None:
    response: Response = await client.get(reverse('get_dish', menu_id, submenu_id, dish_id))
    response_json: dict[str, str | float] = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert response_json['title'] == submenu_data['title']
    assert response_json['description'] == submenu_data['description']
    assert response_json['submenu_id'] == submenu_id


async def test_patch_dish(
        client: AsyncClient,
        dish_update_data: dict[str, str],
        menu_id: str,
        submenu_id: str,
        dish_id: str
) -> None:
    response: Response = await client.patch(
        reverse(
            'update_dish',
            menu_id,
            submenu_id,
            dish_id),
        json=dish_update_data
    )
    response_json: dict[str, str | float] = response.json()

    assert response.status_code == 200
    assert response_json['title'] == dish_update_data['title']
    assert response_json['description'] == dish_update_data['description']
    assert response_json['price'] == dish_update_data['price']


async def test_patch_dish_invalid_id(
        client: AsyncClient,
        dish_update_data: dict[str, str],
        menu_id: str,
        submenu_id: str
) -> None:
    response: Response = await client.patch(
        reverse(
            'update_dish',
            menu_id,
            submenu_id,
            uuid.uuid4()),
        json=dish_update_data
    )

    assert response.status_code == 404


async def test_delete_dish_invalid_id(
        client: AsyncClient,
        menu_id: str,
        submenu_id: str
) -> None:
    response: Response = await client.delete(
        reverse(
            'delete_dish',
            menu_id,
            submenu_id,
            uuid.uuid4()
        )
    )
    assert response.status_code == 404


async def test_delete_dish(client: AsyncClient, menu_id: str, submenu_id: str, dish_id: str) -> None:
    response_dish: Response = await client.delete(reverse('delete_dish', menu_id, submenu_id, dish_id))
    response_submenu: Response = await client.delete(reverse('delete_submenu', menu_id, submenu_id))
    response_menu: Response = await client.delete(reverse('delete_menu', menu_id))

    assert response_dish.status_code == 200
    assert response_menu.status_code == 200
    assert response_submenu.status_code == 200

    remove_environment_variable('menu_id', 'submenu_id', 'dish_id')
