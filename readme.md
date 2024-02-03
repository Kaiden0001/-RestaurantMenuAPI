# Что-то на FastAPI

## Запуск обычных тестов
```bash
sudo docker compose up --build
```

## Запуск pytest
```bash
sudo docker compose -f docker-compose-test.yml up --build -d
```
```bash
sudo docker compose exec web_test pytest -s -v
```
[Третье задание](https://github.com/Kaiden0001/RestaurantMenuAPI/blob/a1de8aaee29bb59771ecdf637f426df5d3c31bf8/src/menu/repositories/menu_repository.py#L34)<br>
[Четвертое задание](https://github.com/Kaiden0001/RestaurantMenuAPI/blob/a1de8aaee29bb59771ecdf637f426df5d3c31bf8/src/menu/tests/test_dish_and_submenu_count.py#L1)

## 3 неделя
### [Аналог reverse()](https://github.com/Kaiden0001/RestaurantMenuAPI/blob/491314d51a04aceeecc00877c06ec954355e48c9/src/menu/tests/utils.py#L30)
