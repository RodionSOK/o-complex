FROM python:3.13-slim

ENV PYTHONPATH="${PYTHONPATH}:/app:/app/src/apps:/app/src/apps/weather/services"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install poetry gunicorn && poetry config virtualenvs.create false && poetry install --no-root

COPY ./src/apps/weather/templates/ ./app/src/apps/weather/templates/

CMD ["gunicorn", "config.mysite.wsgi:application", "--bind", "0.0.0.0:8000"]