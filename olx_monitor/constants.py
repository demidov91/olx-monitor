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

# Keep in DB only last N offers.
MAX_OFFERS_TO_KEEP_IN_DB = 2000

# OLX site constatnts.
PRICE_OLX_PARAM = 'price'
RENT_OLX_PARAM = 'rent'
SPACE_OLX_PARAM = 'm'
ROOMS_OLX_PARAM = 'rooms'