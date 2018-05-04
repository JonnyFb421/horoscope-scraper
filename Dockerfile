FROM python:3.6.5-alpine3.7

RUN apk add --no-cache build-base

ADD . /app/
WORKDIR /app/
RUN pip install .

CMD ["python", "horoscope_scraper/app.py"]