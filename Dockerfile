# Dashboard demo server. Holds only this project's generated data; NASA PSI originals are linked or streamed from
# PSI, and data/raw/ is a transient on-demand cache for timeseries (see demo/server.py).
FROM python:3.12-slim

# uv from PyPI rather than ghcr.io/astral-sh/uv: the deploy host times out reaching ghcr.io.
RUN pip install --no-cache-dir uv==0.12.10
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/opt/venv PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --group server

COPY fif/ fif/
COPY demo/ demo/
COPY docs/ docs/
COPY data/processed/ data/processed/
COPY data/digest/ data/digest/
COPY data/corrections/tests_patches.json data/corrections/tests_patches.json
COPY data/publications/ data/publications/
COPY data/translations/quotes_es.json data/translations/quotes_es.json
COPY data/export/ data/export/
RUN python demo/build_demo.py

RUN useradd --system --uid 10001 --home-dir /app app \
    && mkdir -p /app/data/raw /app/data/board && chown app /app/data/raw /app/data/board
USER app

ENV HOST=0.0.0.0 PORT=8000 FIF_RAW_ROOT=/app/data/raw FIF_RAW_CACHE_MB=300 FIF_BOARD_DB=/app/data/board/board.db
EXPOSE 8000
# Last, so a new commit does not invalidate the cached layers above. /api/health reports them (run.sh sets them).
ARG FIF_COMMIT=unknown
ARG FIF_COMMIT_DATE=unknown
ENV FIF_COMMIT=$FIF_COMMIT FIF_COMMIT_DATE=$FIF_COMMIT_DATE
CMD ["python", "demo/server.py"]
