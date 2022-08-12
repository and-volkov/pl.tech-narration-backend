FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt upgrade -y

RUN apt install ffmpeg -y

COPY requirements-dev.txt .

RUN pip3 install -r requirements-dev.txt --no-cache-dir

ENV PYTHONPATH .

COPY ./ .
