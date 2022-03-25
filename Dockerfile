# syntax=docker/dockerfile:1.2
FROM python:3.9.12-slim AS builder

RUN --mount=type=cache,target=/root/.cache pip install poetry==1.1.12
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache poetry install --no-ansi --no-dev --no-interaction --no-root

FROM python:3.9.12-slim AS runner

ENV ATOTI_DISABLE_TELEMETRY=true
ENV ATOTI_HIDE_EULA_MESSAGE=true
ENV PORT=80

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY app app

ENTRYPOINT ["python", "-u", "-m", "app"]

EXPOSE $PORT
