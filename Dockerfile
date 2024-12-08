FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
        sqlite3 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    -r requirements.txt \
    --upgrade pip

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]