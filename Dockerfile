FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 3001

CMD ["gunicorn", "djmyinfo.wsgi:application", "--bind", "0.0.0.0:3001"]
