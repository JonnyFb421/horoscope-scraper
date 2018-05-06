import pytest

from horoscope_scraper.app import app
from horoscope_scraper.api.api import daily_readings
from horoscope_scraper import get_readings


@pytest.fixture
def client():
    app.config['TESTING'] = True
    yield app.test_client()
#
# def test_daily_readings(client):
#     expected = 'gonna be a damn good day'
#     # def get_mock_class():
#     #     class MockClass:
#     #         def __init__(self, *args):
#     #             pass
#     #         def get_readings(self):
#     #             return expected
#     result = client.get(daily_readings('taurus'))
#
#     # monkeypatch.setattr(get_readings.GetReadings, get_mock_class(expected))
#     assert result == expected



    # def daily_readings(sign):
    #     try:
    #         result = GetReadings(sign).get_readings()
    #     except SignNotFound:
    #         result = {'error': 'Invalid zodiac sign selected.'}
    #     return jsonify(result)
