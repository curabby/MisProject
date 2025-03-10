FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000


CMD ["sh", "-c", "python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    pytest -v --pdb && \
    python manage.py populate_fake_data && \
    python manage.py runserver 0.0.0.0:8000"]

