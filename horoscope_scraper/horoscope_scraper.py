import requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5000
debug = True


@app.route("/")
def display_all_signs():
    return "Select your sign: do later..."

def search_for_horoscopes():
    response = requests.get('https://www.astrologyzone.com/forecasts/taurus-horoscope-for-april-2018/')
    if response.ok:
        soup = BeautifulSoup(response.content)
        horoscope = soup.find_all(
            "div", {"class": "article horoscope-content"}
        )



if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
