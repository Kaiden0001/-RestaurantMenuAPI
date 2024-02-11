import gspread
from gspread import Client, Spreadsheet

from src.config import BASE_DIR, SPREADSHEET_URL
from src.menu.worker.celery_app import celery_app
from src.menu.worker.tasks.utils.check_data import (
    check_dish_data,
    check_menu_data,
    check_submenu_data,
    delete_dishes,
    delete_menus,
    delete_submenus,
)
from src.menu.worker.tasks.utils.menu_parser import get_full_menu
from src.menu.worker.tasks.utils.parse_sheet import parse_sheet


def get_values() -> list[list]:
    """
    Получает данные из Google Sheets.

    :return: Список списков значений из листа таблицы.
    """
    client: Client = gspread.service_account(BASE_DIR / 'service_account.json')
    sh: Spreadsheet = client.open_by_url(SPREADSHEET_URL)
    values: list[list] = sh.sheet1.get_all_values()
    return values


@celery_app.task()
def sync_excel_to_db():
    try:
        values: list[list] = get_values()

        menu_data_offline, submenu_data_offline, dish_data_offline = parse_sheet(values)
        menu_data_online, submenu_data_online, dish_data_online = get_full_menu()

        delete_dishes(dish_data_online, dish_data_offline)
        delete_submenus(submenu_data_online, submenu_data_offline)
        delete_menus(menu_data_online, menu_data_offline)

        check_menu_data(menu_data_online, menu_data_offline)
        check_submenu_data(submenu_data_online, submenu_data_offline)
        check_dish_data(dish_data_online, dish_data_offline)
    except FileNotFoundError:
        print('No such file')
    except IndexError:
        print('Check sheet')
    except Exception as e:
        print('Exception: ', e)
