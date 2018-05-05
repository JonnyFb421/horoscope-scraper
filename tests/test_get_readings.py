import tempfile

import pytest
from ruamel import yaml

from horoscope_scraper.get_readings import GetReadings
from horoscope_scraper.exceptions import SignNotFound


def test_get_readings_init_with_bad_sign():
    with pytest.raises(SignNotFound):
        GetReadings('uhnope')


def test_get_readings_init_config_not_none():
    result = GetReadings('taurus').config
    assert result is not None


def test_get_valid_signs():
    expected = [
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "leo",
        "virgo",
        "libra",
        "scorpio",
        "sagittarius",
        "capricorn",
        "aquarius",
        "pisces"
    ]
    result = GetReadings('pisces').get_valid_signs()
    for sign in result:
        assert sign in expected


def test_set_sign_with_valid_sign():
    sign = 'pisCes'
    result = GetReadings(sign).get_valid_signs()
    assert result == sign
