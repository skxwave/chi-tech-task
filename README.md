# Flask API
This is a Flask-based REST API that provides a role-based permission system, user management, and article management. The application is containerized using Docker and uses PostgreSQL as the database.

## Features

1. Role-based permissions
2. JWT Authentication. Only admin can create new users
3. Postgresql with SQLAlchemy ORM
4. Swagger docs using [Flasgger](https://github.com/flasgger/flasgger)
5. Tests using Pytest. Coverage >80%
6. Fully containerized using Docker and Docker compose

## Getting started with Docker

1. Clone the repository:
```bash
$ git clone https://github.com/skxwave/chi-tech-task.git
```
2. Build and raise container:
```bash
$ docker-compose up --build
```

## Install and Run Manually

1. Clone the repository and navigate to the project directory:
```bash
$ git clone https://github.com/skxwave/chi-tech-task.git
$ cd chi-tech-task
```
2. Create and activate enviroment:
```bash
$ python -m venv .venv
$ .\.venv\Scripts\activate
$ # for linux
$ source .venv/bin/activate
```
3. Install poetry and dependencies:
```bash
$ pip install poetry
$ poetry install
```
4. Copy .env.template and set your values:
```bash
$ cp .env.template .env
```
5. Migrate database
```bash
$ alembic upgrade head
```
6. Seed db with admin user and some test data:
```bash
$ python entrypoint.sh
```
7. Start the app:
```bash
$ python main.py
```

## Tests

All tests are written using ```pytest```. Run tests:
```bash
$ pytest
$ # Use --cov to see coverage
$ pytest --cov
```