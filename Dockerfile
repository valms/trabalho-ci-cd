# Estágio 1: Build
FROM python:3.13-alpine AS builder

RUN apk add --no-cache build-base libffi-dev

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# Estágio 2: Run
FROM python:3.13-alpine AS runtime

RUN apk update && apk upgrade --no-cache

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src ./src

RUN adduser -D appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.concilia_core.main:app", "--host", "0.0.0.0", "--port", "8000"]