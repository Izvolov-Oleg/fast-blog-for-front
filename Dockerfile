FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

RUN apt-get update
RUN apt-get -y install gcc

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . ./

CMD ["uvicorn", "app.main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]

