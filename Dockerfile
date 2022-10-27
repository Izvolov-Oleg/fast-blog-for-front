FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

RUN apt-get update && apt-get -y install gcc

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]

COPY . ./


