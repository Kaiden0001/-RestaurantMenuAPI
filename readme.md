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
[Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос](https://github.com/Kaiden0001/RestaurantMenuAPI/blob/a1de8aaee29bb59771ecdf637f426df5d3c31bf8/src/menu/repositories/menu_repository.py#L23)<br>
[Реализовать тестовый сценарий](https://github.com/Kaiden0001/RestaurantMenuAPI/blob/a1de8aaee29bb59771ecdf637f426df5d3c31bf8/src/menu/tests/test_dish_and_submenu_count.py#L1)<br>
[Аналог reverse()](https://github.com/Kaiden0001/RestaurantMenuAPI/blob/491314d51a04aceeecc00877c06ec954355e48c9/src/menu/tests/utils.py#L30)<br>
[Обновление меню из google sheets раз в 15 сек]()<br>
[Блюда по акции. Размер скидки (%) указывается в столбце G файла]()<br>

Menu sheet
https://docs.google.com/spreadsheets/d/1egA1F7sk3z5LPLhlijMnyZMYTaZrX_7yqv0ulhcZQb0/edit?usp=sharing
