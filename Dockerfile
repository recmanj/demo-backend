FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml ./
RUN uv pip install --system --no-cache -r pyproject.toml

COPY alembic.ini ./
COPY migrations/ migrations/
COPY src/ src/

EXPOSE 8000
ENV PYTHONPATH=/app/src

CMD ["sh", "-c", "alembic upgrade head && uvicorn demo_backend.main:app --host 0.0.0.0 --port 8000"]
