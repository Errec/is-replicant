FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

# Copy pyproject.toml from the root directory
COPY ../../pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Install spaCy model
RUN pip install spacy && python -m spacy download en_core_web_sm

COPY . /app

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
