import os


CITIES_URL = 'https://olx.pl/api/v1/geo-encoder/regions/{region_id}/cities/'
DISTRICTS_URL = 'https://olx.pl/api/v1/geo-encoder/cities/{city_id}/districts/' # most prob, we don't need it


CURRENT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CURRENT_DIR, 'data')


HELP_MESSAGE = (
    "Оберіть фільтри для пошуку квартир на сторінці https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/ , "
    "скопіюйте адресу сторінці після обрання фільтрів та надішліть її боту. "
    "Він буде постійно досилати вам оновлення, поки не відправите команду /stop\n\n{filter_message}"
)

# Actually, Telegram Bot API supports up to 10 photos in a media group but it sometimes fails to send them.
MAX_PHOTOS_TO_SEND = 8