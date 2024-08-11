# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    apt-get clean

# install the requirements
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080/tcp

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]