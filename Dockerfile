FROM python:3.9-slim AS builder

RUN --mount=type=cache,target=/root/.cache pip install poetry==1.1.10
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml .

RUN --mount=type=cache,target=/root/.cache poetry install --no-ansi --no-dev

FROM python:3.9-slim AS runner

ENV ATOTI_DISABLE_TELEMETRY=true

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY app app

ENTRYPOINT ["python", "-u", "-m", "app"]
