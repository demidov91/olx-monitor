import os


CITIES_URL = 'https://olx.pl/api/v1/geo-encoder/regions/{region_id}/cities/'
DISTRICTS_URL = 'https://olx.pl/api/v1/geo-encoder/cities/{city_id}/districts/' # most prob, we don't need it


CURRENT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CURRENT_DIR, 'data')