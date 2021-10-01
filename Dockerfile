# syntax=docker/dockerfile:experimental
# Enables Docker buildkit caching feature, also requires setting DOCKER_BUILDKIT=1
FROM python:3.9-slim AS builder

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .

RUN --mount=type=cache,target=/root/.cache poetry install --no-ansi


FROM python:3.9-slim AS runner

ENV ATOTI_DISABLE_TELEMETRY=true

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY app app

ENTRYPOINT ["python", "-u", "-m", "app"]
