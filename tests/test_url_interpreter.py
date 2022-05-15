import pytest

from olx_monitor.url_interpreter import browser_url_to_api


@pytest.mark.parametrize('browser, api', [
    (
        'https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/?search%5Bfilter_float_m:from%5D=40',
        'https://www.olx.pl/api/v1/offers/?region_id=3&city_id=19701&filter_float_m%3Afrom=40'
        '&offset=0&limit=40&category_id=15&facets=[{"field"%3A"district"%2C"fetchLabel"%3Atrue%2C"fetchUrl"%3Atrue%2C"limit"%3A10}]'
    ),
    (
        'https://www.olx.pl/d/nieruchomosci/mieszkania/biale-blota_41973/',
        'https://www.olx.pl/api/v1/offers/?region_id=15&city_id=41973'
        '&offset=0&limit=40&category_id=15&facets=[{"field"%3A"district"%2C"fetchLabel"%3Atrue%2C"fetchUrl"%3Atrue%2C"limit"%3A10}]',
    ),
])
def test_browser_url_to_api(browser, api):
    assert browser_url_to_api(browser) == api


