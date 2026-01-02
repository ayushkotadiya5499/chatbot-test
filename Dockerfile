FROM python:3.11-slim


WORKDIR /app

COPY .env /app/.env

# Python optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy poetry files first (for caching)
COPY pyproject.toml poetry.lock ./

# Install only dependencies (NOT the project itself)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY chat_front.py chat_backend.py ./

# Streamlit default port
EXPOSE 8501

RUN chmod -R 777 /app


VOLUME ["/app/data"]

# Run Streamlit
CMD ["streamlit", "run", "chat_front.py"]
