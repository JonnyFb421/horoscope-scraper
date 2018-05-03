import requests
from flask import Flask
from flask import render_template
from flask import jsonify
from flask_bootstrap import Bootstrap

from horoscope_scraper.get_readings import GetReadings

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)

HOST = '127.0.0.1'
PORT = 5000
debug = True


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/readings/<sign>")
def endpoint_display_readings(sign):
    return jsonify(GetReadings(sign).get_readings())


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
