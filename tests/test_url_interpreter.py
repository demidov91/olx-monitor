import pytest

from olx_monitor.url_interpreter import browser_url_to_api, query_to_params


@pytest.mark.parametrize('browser, api', [
    (
        'https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_m:from%5D=40',
        'https://www.olx.pl/api/v1/offers/?region_id=3&city_id=19701&filter_float_m%3Afrom=40'
        '&offset=0&limit=10&category_id=15&facets=[{"field"%3A"district"%2C"fetchLabel"%3Atrue%2C"fetchUrl"%3Atrue%2C"limit"%3A10}]'
    ),
    (
        'https://www.olx.pl/d/nieruchomosci/mieszkania/biale-blota_41973/',
        'https://www.olx.pl/api/v1/offers/?region_id=15&city_id=41973'
        '&offset=0&limit=10&category_id=15&facets=[{"field"%3A"district"%2C"fetchLabel"%3Atrue%2C"fetchUrl"%3Atrue%2C"limit"%3A10}]',
    ),
])
def test_browser_url_to_api(browser, api):
    assert browser_url_to_api(browser) == api


@pytest.mark.parametrize('browser_qs, api_params', [
    (
        'search%5Bfilter_float_m:from%5D=40',
        {'filter_float_m:from': '40'},
    ),
    (
        '',
        {},
    ),
    (
        'search[private_business]=private&search[filter_float_price:from]=1000&search[filter_float_price:to]=3200&'
        'search[filter_enum_furniture][0]=yes&search[filter_float_m:from]=34&search[filter_float_m:to]=50&'
        'search[filter_enum_rooms][0]=one&search[filter_enum_rooms][1]=two',
        {
            'filter_enum_furniture[0]': 'yes',
            'filter_enum_rooms[0]': 'one',
            'filter_enum_rooms[1]': 'two',
            'filter_float_m:from': '34',
            'filter_float_m:to': '50',
            'filter_float_price:from': '1000',
            'filter_float_price:to': '3200',
            'owner_type': 'private'
        },
    ),
])
def test_query_to_params(browser_qs, api_params):
    assert query_to_params(browser_qs) == api_params