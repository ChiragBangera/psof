# Stage 1: Base Image
ARG ENVIRONMENT

FROM python:3.13-alpine AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN addgroup -S myapp && adduser -S -G myapp user -u 1234
RUN mkdir -p /usr/src/app
WORKDIR /usr/src

# Stage 2: Dependencies Installtion
FROM base AS dependencies
COPY pyproject.toml uv.lock ./
RUN if [ "$ENVIRONMENT" = "test" ]; then uv sync --frozen --no-cache --only -dev --link-mode=copy; \
    else uv sync --frozen --no-cache --no-dev; fi

# Stage 3: Build Application
FROM base AS builder
COPY --from=dependencies /usr/src/.venv /usr/src/.venv
COPY --chown=user:myapp app ./app

# Stage 4: Final Runtime Image
FROM base AS final
# ENV UV_LINK_MODE=copy
# ENV PATH="/usr/src/.venv/bin:$PATH"
USER user
COPY --from=builder /usr/src /usr/src
CMD [ "uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]

