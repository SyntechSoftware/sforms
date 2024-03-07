FROM python:3.11-alpine
WORKDIR /app

RUN apk add --no-cache gcc make musl-dev linux-headers bash

COPY ./requirements.txt .
RUN pip install -r /app/requirements.txt

COPY . .

CMD "./manage.py runserver 0.0.0.0:8000"

EXPOSE 8000
