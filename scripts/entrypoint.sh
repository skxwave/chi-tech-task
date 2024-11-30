#!/bin/sh
poetry run alembic upgrade head
exec "$@"
poetry run python seed_db.py