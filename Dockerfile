FROM python:3.6.5-alpine3.7

ADD . /app/
WORKDIR /app/
RUN pip install .

ENTRYPOINT ['start-horoscope-scraper']