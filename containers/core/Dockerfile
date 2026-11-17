FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./
COPY services/core/pyproject.toml services/core/README.md ./services/core/
COPY services/core/src ./services/core/src

RUN uv sync --frozen --package sgd3dgs-core --extra api --no-dev

EXPOSE 8080

CMD ["uv", "run", "--no-sync", "uvicorn", "sgd3dgs_core.api:app", "--host", "0.0.0.0", "--port", "8080"]
