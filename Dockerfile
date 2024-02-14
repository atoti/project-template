# syntax=docker/dockerfile:1.2
FROM python:3.9.18-slim AS builder

ENV POETRY_VENV_PATH=/usr/local/poetry
RUN python -m venv $POETRY_VENV_PATH
RUN $POETRY_VENV_PATH/bin/pip install poetry==1.7.1

COPY poetry.lock pyproject.toml ./

RUN POETRY_VIRTUALENVS_CREATE=false $POETRY_VENV_PATH/bin/poetry install --no-cache --no-root --only main --sync

FROM python:3.9.18-slim AS runner

ENV ATOTI_HIDE_EULA_MESSAGE=true
ENV PORT=80

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY app app

ENTRYPOINT ["python", "-u", "-m", "app"]

EXPOSE $PORT
