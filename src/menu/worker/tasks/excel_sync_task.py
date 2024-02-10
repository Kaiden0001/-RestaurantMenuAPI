import time

from src.menu.worker.celery_app import celery_app


@celery_app.task
def test_celery():
    print(time.time())
