FROM python:3.10-slim 

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN mkdir -p /app

COPY src/ /app
COPY poetry.lock /app
COPY pyproject.toml /app

WORKDIR /app

RUN poetry install --without dev
ENV ENVIRONMENT_NAME DEV
ENV AWS_REGION us-east-1
ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8080"]