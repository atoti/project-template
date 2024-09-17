# Inspired from https://github.com/astral-sh/uv-docker-example/blob/dee88a8c43be3b16b0ad58f0daee5eaee7e2157a/multistage.Dockerfile.

FROM ghcr.io/astral-sh/uv:0.4.10-python3.10-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /venv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

# Keep this synced with the builder image.
FROM python:3.10-slim-bookworm

COPY --from=builder /venv app

ENV PATH="/app/.venv/bin:$PATH"

COPY app app

ENV ATOTI_HIDE_EULA_MESSAGE=true
ENV PORT=80

EXPOSE $PORT

CMD ["python", "-u", "-m", "app"]
