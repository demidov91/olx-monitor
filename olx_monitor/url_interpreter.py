import json
import re
import os
from urllib import parse

from olx_monitor.exceptions import UnexpectedUrlFormat
from olx_monitor.constants import DATA_DIR

like_an_url_pattern = re.compile(r'https://(m\.)?olx.pl/.+?')
browser_url_path_pattern = re.compile(
    r'(/d)?/nieruchomosci/mieszkania/(wynajem/)?(?P<normalized_city>[\w_-]*)/?'
)
qs_param_pattern = re.compile(r'search\[(?P<name>.*?)\](?P<index>\[\d+\])?')


def browser_url_to_api(browser_url: str):
    try:
        parsed_url = parse.urlparse(browser_url)
        params = path_to_params(parsed_url.path)
        params.update(query_to_params(parsed_url.query))
        return build_api_url(params)
    except UnexpectedUrlFormat as e:
        e.url = browser_url
        raise e


def path_to_params(path: str):
    match = browser_url_path_pattern.match(path)
    if match is None:
        raise UnexpectedUrlFormat(path=path)

    city_name = match.group('normalized_city')

    return city_to_params(city_name)


def city_to_params(city_name: str):
    if not city_name:
        return {}

    with open(os.path.join(DATA_DIR, 'cities.json'), 'rb') as f:
        cities = json.load(f)

    try:
        return {
            'region_id': cities[city_name]['region-id'],
            'city_id': cities[city_name]['id'],
        }
    except KeyError as e:
        raise UnexpectedUrlFormat(city_name=e.args[0])


def query_to_params(query_string: str):
    parsed_qs = {}

    for key, value in parse.parse_qsl(query_string):
        match = qs_param_pattern.match(key)
        if match is None:
            raise UnexpectedUrlFormat(qs_param=key)

        parsed_qs[match.group('name') + (match.group('index') or '')] = value

    if 'private_business' in parsed_qs:
        parsed_qs['owner_type'] = parsed_qs.pop('private_business')

    return parsed_qs


def build_api_url(params: dict):
    params['offset'] = 0
    params['limit'] = 10
    params['category_id'] = 15
    params['facets'] = '[{"field"%3A"district"%2C"fetchLabel"%3Atrue%2C"fetchUrl"%3Atrue%2C"limit"%3A10}]'
    return 'https://www.olx.pl/api/v1/offers/?' + parse.urlencode(params, safe='[]{}"%')

