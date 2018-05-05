Horoscope Scraper
===

What is it?
---
[Horoscope Scraper](http://52.14.201.238/) is a Flask application that aggregates daily horoscope readings into a single page.  


How does it work?
---
Horoscope Scraper uses [ScrapeIt](https://github.com/JonnyFb421/scrapeit) to retrieve text from various websites that 
display daily horoscope readings.  The [config](./horoscope_scraper/config/pages.yaml) is how the application determines
where to go and what text to grab.  The application consists only two routes: index and 

How do I run it?
---
Start by installing the application.  While in the project root run:
```bash
pip3 install -e .[dev]
```
You can run the Flask server natively by running:
```bash
python3 ./horoscope_scraper/app.py
```
Or you can start the server inside of a Docker container:
```bash
docker build -t horoscope-scraper:1.0.0 .
docker run -p 80:5000 horoscope-scraper:1.0.0
```
After the server is running, navigate to [http://localhost/](http://localhost/) or [http://0.0.0.0/](http://0.0.0.0/)`.

How do I run the tests?
---
Tests are written with pytest.  The tests can be started by running:
```bash
pytest 
```

Okay, but why?
---
I hypothesized by aggregating daily horoscope readings it would be very easy to point out the inconsistent themes for 
a single zodiac sign in a day.
