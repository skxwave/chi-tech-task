FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl git build-essential libpq-dev \
    && apt-get clean

# Poetry install
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy & configure project
COPY . .
ENV FLASK_APP=main.py
EXPOSE 5000
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]