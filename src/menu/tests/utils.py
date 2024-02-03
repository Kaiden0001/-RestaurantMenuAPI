import re

from src.main import app


def _replace_path_params(url_path: str, replacements: dict) -> str:
    """
    Заменяет параметры в пути URL значениями из словаря replacements.

    :param url_path: Исходный путь URL с параметрами вида {param}.
    :param replacements: Словарь значений для замены.
    :return: Строка с замененными параметрами.
    """
    for param in replacements:
        url_path = url_path.replace(f'{{{param}}}', str(replacements[param]))
    return url_path


def _extract_path_params(url_path: str) -> list[str]:
    """
    Извлекает имена параметров из пути URL.

    :param url_path: Путь URL с параметрами вида {param}.
    :return: Список имен параметров.
    """
    pattern = re.compile(r'{([^{}]+)}')
    return re.findall(pattern, url_path)


def reverse(func_name: str, *args) -> str:
    """
    Возвращает URL для указанного маршрута, подставляя значения параметров из args.
    Примеры:
        reverse('delete_menu', menu_id)
        reverse('get_menus')
    *если переопредели имя ручки, то указываем новое
    :param func_name: Имя маршрута.
    :param args: Значения параметров в порядке их появления в URL.
    :return: Строка с сформированным URL.
    """
    routers: dict[str, str] = {item.name: item.path for item in app.routes}

    route_path: str | None = routers.get(func_name)
    if not route_path:
        raise ValueError(f"Route with name '{func_name}' not found.")

    params: list[str] = _extract_path_params(route_path)

    if len(params) != len(args):
        raise ValueError(f'Expected {len(params)} arguments, but got {len(args)}.')

    replacements: dict[str, str] = dict(zip(params, map(str, args)))
    result: str = _replace_path_params(route_path, replacements)

    return result
