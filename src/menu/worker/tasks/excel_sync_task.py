import asyncio

from aioredis import from_url

from src.database import REDIS_URL, async_session_maker
from src.menu.services.sheet_service import SheetService
from src.menu.worker.celery_app import celery_app


async def sync_db_sheet():
    async with async_session_maker() as session:
        try:
            redis = from_url(REDIS_URL)
            sheet_service = SheetService(redis, session)
            await sheet_service.check_data()
            print('SYNC')
        except IndexError as e:
            print('Ошибка', e)


@celery_app.task()
def sync_excel_to_db() -> None:
    """
    Синхронизирует данные из Google Sheets с базой данных.

    Получает данные из Google Sheets, парсит их, получает текущие данные из базы данных,
    затем сравнивает и обновляет базу данных в соответствии с данными из таблицы.

    Обработчик исключений добавлен для обработки ошибок, таких как отсутствие файла,
    некорректное содержимое таблицы или другие исключения, которые могут возникнуть при работе с данными.

    :raises FileNotFoundError: Если файл не найден.
    :raises IndexError: Если произошла ошибка в структуре таблицы.
    """
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(sync_db_sheet())
        return result
    except FileNotFoundError:
        print('No such file')
    except IndexError:
        print('Check sheet')
    except Exception as e:
        print('Exception: ', e)
