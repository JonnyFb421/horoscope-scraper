from flask import Blueprint, jsonify

from horoscope_scraper.get_readings import GetReadings
from horoscope_scraper.exceptions import SignNotFound

api = Blueprint('api', 'api', url_prefix='/api')


@api.route("/v1/daily-readings/<sign>")
def daily_readings(sign):
    try:
        result = GetReadings(sign).get_readings()
    except SignNotFound:
        result = {'error': 'Invalid zodiac sign selected.'}
    return jsonify(result)
