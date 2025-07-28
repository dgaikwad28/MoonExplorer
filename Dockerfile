FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV GUNICORN_WORKERS 3

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# set workdir
WORKDIR /app

# Install requirements
COPY ./requirements/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --no-deps -v -r /tmp/requirements.txt

# change the onershp of the app directory
RUN groupadd --gid 10000 app \
    && useradd --uid 10001 --gid app --shell /bin/bash -c 'app user' -m app \
    && chown -R app:app /app

COPY --chown=app:app . .


EXPOSE 8000

USER app

CMD ["sh", "-c", "uvicorn --host 0.0.0.0 --port 8000 --workers ${UVICORN_WORKERS} app.main:app"]
