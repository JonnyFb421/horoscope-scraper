import re
import os
import logging
import pkg_resources

import requests
from requests import HTTPError
from ruamel import yaml
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)


def parse_text_with_regex(start, end, text):
    """
    Searches blob of text and grabs the text between start and end
    :param start: String pattern to start matching after
    :param end: String pattern to stop matching before
    :param text: String text to search
    :return: String the match or original text
    """
    re_pattern = f"(?<={start}).*?(?={end})"
    re_match = re.search(re_pattern, text, re.DOTALL)
    if re_match:
        return re_match[0]
    else:
        return text


def get_soup(content):
    """
    Return a BeautifulSoup4 object.
    :param content: String containing HTML
    :return: bs4 object
    """
    return BeautifulSoup(content, "html.parser")


def get_text_from_single_tag(soup, tag, selector):
    """
    Returns text from the first element that matches tag and selector.
    :param soup: bs4 object
    :param tag: String HTML tag name
    :param selector: Dict property and value to identify the tag
    :return: String text from the matching element
    """
    return soup.find(
        tag,
        selector
    ).get_text().strip()


def get_text_from_many_tags(soup, tag, selector):
    """
    Returns text from any element that matches tag and selector.
    :param soup: bs4 object
    :param tag: String HTML tag name
    :param selector: Dict property and value to identify the tag
    :return: String containing text from all matching elements
    """
    matching_text = ''
    potential_matches = soup.findAll(
        tag,
        selector
    )
    for match in potential_matches:
        matching_text += match.get_text().strip()
    return matching_text


def get_target_from_soup(soup, **kwargs):
    """
    Uses the config to retrieve the desired text from the soup.
    :param soup: bs4 object
    :param kwargs: yaml config file
    :return: String text from the matching elements
    """
    if kwargs['selector_is_unique']:
        horoscope = get_text_from_single_tag(
            soup,
            kwargs['selector'][0],
            kwargs['selector'][1]
        )
    else:
        horoscope = get_text_from_many_tags(
            soup,
            kwargs['selector'][0],
            kwargs['selector'][1]
        )
    if kwargs['use_regex']:
        horoscope = parse_text_with_regex(
            kwargs['match_start'],
            kwargs['match_end'],
            horoscope
        )
    return horoscope


def make_request(url):
    """
    Make GET request to url
    :param url: String URL to load
    :return: requests object
    """
    headers = {
        'User-Agent':
            "Mozilla/5.0"
            " (Windows NT 10.0; Win64; x64; rv:59.0)"
            " Gecko/20100101 Firefox/59.0"
    }
    return requests.get(url, headers=headers)


def grab_text_from_web(url_key, **kwargs):
    """
    Use this method to return text from a matching selector
    :param url_key: String key to urls dictionary
    :param kwargs: yaml config file
    :return: String text from the matching elements
    """
    url = kwargs['urls'][url_key]
    response = make_request(url)
    if response.ok:
        soup = get_soup(response.content)
        matching_text = get_target_from_soup(soup, **kwargs)
    else:
        raise HTTPError(f"Received {response.status_code} from {url}")
    if matching_text:
        return matching_text.replace('\n', '').strip()
    else:
        logging.error(f'The selector or regex for {url} returned no matches!')


config_file = pkg_resources.resource_filename(__name__, 'config/pages.yaml')
sign = 'taurus'

with open(config_file) as file:
    config = yaml.safe_load(file)

for website in config:
    reading = grab_text_from_web(sign, **config[website])
    print(f'```{reading}```')
