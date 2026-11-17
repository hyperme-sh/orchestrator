FROM python:3.13-alpine@sha256:9ef1a599f863231c3d91e941389bfdc4a2d6070557243d54df1a4e57015b960e AS build
COPY --from=ghcr.io/astral-sh/uv:0.11.26@sha256:3d868e555f8f1dbc324afa005066cd11e1053fc4743b9808ca8025283e65efa5 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock LICENSE NOTICE ./
COPY src src
RUN uv sync --frozen --no-dev --no-editable
FROM python:3.13-alpine@sha256:9ef1a599f863231c3d91e941389bfdc4a2d6070557243d54df1a4e57015b960e
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY LICENSE NOTICE /usr/share/licenses/hypermesh-orchestrator/
ARG SOURCE_SHA
ARG BUILT_AT
LABEL org.opencontainers.image.source="https://github.com/hyperme-sh/hypermesh-orchestrator" \
      org.opencontainers.image.revision="${SOURCE_SHA}" \
      org.opencontainers.image.licenses="Apache-2.0"
USER 65532:65532
ENTRYPOINT ["/app/.venv/bin/hypermesh-orchestrator"]
