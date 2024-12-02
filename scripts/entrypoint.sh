#!/bin/sh
poetry run alembic upgrade head
poetry run flask admin seed_db
poetry run gunicorn main:app --workers 4 --bind 0.0.0.0:5000
exec "$@"