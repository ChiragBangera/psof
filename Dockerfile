FROM python:3.13-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir -p /usr/src/app/app

WORKDIR /usr/src/app

COPY pyproject.toml uv.lock main.py ./

COPY app ./app

RUN uv sync --frozen --no-cache

CMD [ "uv","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


