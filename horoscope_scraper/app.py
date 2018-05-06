from flask import Flask
from flask_bootstrap import Bootstrap

from horoscope_scraper.api.api import api
from horoscope_scraper.views.views import index_blueprint

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(index_blueprint)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
Bootstrap(app)

HOST = '0.0.0.0'
PORT = 5000
debug = True


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
