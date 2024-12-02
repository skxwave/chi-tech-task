# Flask API
This is a Flask-based REST API that provides a role-based permission system, user management, and article management. The application is containerized using Docker and uses PostgreSQL as the database.

## Features

1. **Role-based** permissions
2. **JWT Authentication**
3. PostgreSQL with **SQLAlchemy ORM**
4. Swagger docs using **[Flasgger](https://github.com/flasgger/flasgger)**
5. Tests using Pytest. Coverage >80%
6. Fully containerized using **Docker** and **Docker compose**

## Requirements

- Docker
- Python ^3.12
- PostgreSQL
- Poetry

## Getting started with Docker

1. Clone the repository:
```bash
$ git clone https://github.com/skxwave/chi-tech-task.git
```
2. Copy ```.env.template``` and set up your environment variables:
```bash
$ cp .env.template .env
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
```
For linux users:
```bash
$ source .venv/bin/activate
```
3. Install poetry and dependencies:
```bash
$ pip install poetry
$ poetry install
```
4. Copy ```.env.template``` and set up your environment variables:
```bash
$ cp .env.template .env
```
5. Migrate database
```bash
$ alembic upgrade head
```
6. Create admin user:
```bash
$ flask admin create_user
```
7. (Optional) Seed db with sample data:
```bash
$ flask admin seed_db
```
8. Start the app:
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