#!/bin/sh

wait-for-it db:5432 --timeout=60

alembic upgrade head

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
