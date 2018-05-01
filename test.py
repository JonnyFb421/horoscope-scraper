import re
import os
import pkg_resources

import requests
from requests import HTTPError
from ruamel import yaml
from bs4 import BeautifulSoup


def parse_text_with_regex(start, end, text):
    re_pattern = f"(?<={start}).*?(?={end})"
    re_match = re.search(re_pattern, text, re.DOTALL)
    if re_match:
        return re_match[0]
    else:
        return text


def search_for_horoscopes(sign, **kwargs):
    headers = {
        'User-Agent':
            "Mozilla/5.0"
            " (Windows NT 10.0; Win64; x64; rv:59.0)"
            " Gecko/20100101 Firefox/59.0"
    }
    all_horoscopes = []
    url = kwargs['urls'][sign]
    horoscope = ''
    response = requests.get(url, headers=headers)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        if kwargs['selector_is_unique']:
            horoscope = soup.find(
                kwargs['selector'][0],
                kwargs['selector'][1]
            ).get_text().strip()
        else:
            potential_matches = soup.findAll(
                kwargs['selector'][0],
                kwargs['selector'][1]
            )
            for match in potential_matches:
                horoscope += match.get_text().strip()
        if kwargs['use_regex']:
            horoscope = parse_text_with_regex(kwargs['match_start'], kwargs['match_end'], horoscope)
        if horoscope:
            all_horoscopes.append(horoscope)
        else:
            print(f'something went terribly wrong with {url}')
    else:
        raise HTTPError(f"Received {response.status_code} from {url}")
    return all_horoscopes


config_file = pkg_resources.resource_filename(__name__, os.path.join('config', 'pages.yaml'))
config_file = os.path.join('horoscope_scraper', 'config', 'pages.yaml')
sign = 'pisces'
with open(config_file) as file:
    config = yaml.safe_load(file)

for website in config:
    reading = search_for_horoscopes(sign, **config[website])[0]
    print(f'```{reading}```')