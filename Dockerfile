# First stage to install dependencies
FROM python:3.9-slim AS builder

ENV ATOTI_DISABLE_TELEMETRY=true
ENV PIP_CACHE_DIR=true

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-ansi
RUN rm -rf ~/.cache/pypoetry

# Second stage to copy project code and resources

FROM python:3.9-slim

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY app app

ENTRYPOINT ["python", "-u", "-m", "app"]
