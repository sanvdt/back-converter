FROM python:3.11

RUN apt-get update && apt-get install -y ghostscript poppler-utils libreoffice

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV REDIS_URL=redis://redis:6379
ENV PYTHONPATH=/app

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV REDIS_URL=redis://redis:6379
ENV PYTHONPATH=/app
