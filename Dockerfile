# Python-Basisimage
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    npm \
    build-essential \
    gettext \
    curl \
    redis-server \
    libmagic1 \
    sqlite3 \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use either git clone (commented) or COPY for local development
#RUN git clone https://github.com/liqd/adhocracy-plus.git .
COPY . .

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

RUN npm install && \
    npm run build:prod && \
    pip install --upgrade pip && \
    pip install psycopg-c==3.1.19 && \
    pip install -r requirements.txt

RUN make install && \
    make fixtures

RUN make test

ENV DJANGO_SETTINGS_MODULE=adhocracy-plus.config.settings.dev
ENV PYTHONUNBUFFERED=1
ENV DATABASE=sqlite3
ENV DJANGO_DEBUG=True
ENV DJANGO_SECRET_KEY=dummy_key_for_development

# 10.0.2.2 is the IP address of the android emulator
RUN echo "SECRET_KEY = \"${DJANGO_SECRET_KEY}\"" > adhocracy-plus/config/settings/local.py && \
    echo "ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '10.0.2.2']" >> adhocracy-plus/config/settings/local.py

EXPOSE 8004

# Run migrations and start server directly
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8004
