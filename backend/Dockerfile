FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml ./
COPY app_builder_ai ./app_builder_ai
RUN pip install --no-cache-dir .

EXPOSE 8100
CMD ["uvicorn", "app_builder_ai.main:app", "--host", "0.0.0.0", "--port", "8100"]
