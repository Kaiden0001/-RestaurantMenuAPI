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