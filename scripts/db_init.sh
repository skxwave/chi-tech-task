#!/bin/bash

poetry run alembic upgrade head

poetry run python seed_db.py