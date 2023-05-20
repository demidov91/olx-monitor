import pytest

@pytest.fixture
def olx_offer():
    return {
		"id": 654667240,
		"url": "https://www.olx.pl/d/oferta/2-pokoje-plac-grunwaldzki-od-zaraz-promocja-v-ix-2023-CID3-IDIiUR2.html",
		"title": "2 pokoje - Plac Grunwaldzki - od zaraz - promocja V-IX 2023!",
		"last_refresh_time": "2023-05-20T11:32:37+02:00",
		"created_time": "2021-01-28T14:17:54+01:00",
		"valid_to_time": "2023-05-31T21:38:48+02:00",
		"pushup_time": "2023-05-20T11:32:37+02:00",
		"omnibus_pushup_time": "2023-05-20T11:32:37+02:00",
		"description": "[English below) <br />\n<br />\nDo wynajęcia od zaraz mieszkanie w samym centrum Wrocławia – przy ulicy Roentgena, zaraz obok Pl. Grunwaldzkiego, w pobliżu siedziby wielu firm i uczelni (PWr, UP, AM). W zasięgu ręki pełna infrastruktura - tramwaje, autobusy, sklepy itd. <br />\n<br />\nKlatka schodowa jest świeżo po remoncie, zamykana. <br />\n<br />\nMieszkanie znajduje się na 2. piętrze, ma 48 m2, składa się z dwóch pokoi (duży salon i sypialnia), niedawno wyremontowanej kuchni, małej łazienki i przedpokoju.  <br />\n<br />\nOgrzewane oszczędnymi, elektrycznymi piecami akumulacyjnymi. W pełni umeblowane i wyposażone. Mieszkanie będzie generalnie sprzątnięte bezpośrednio przed wprowadzeniem się nowych lokatora/ów. <br />\n<br />\nIdealne dla pary lub dla 2+1. <br />\n<br />\nWynajem: 2900 zł plus opłaty 800 zł (gaz, prąd, Internet i kablówka z UPC, woda, czynsz). <br />\nUwaga: możliwość negocjacji niższej ceny za miesiące maj-wrzesień 2023. <br />\n<br />\nZapraszam do obejrzenia mieszkania :-) <br />\n<br />\nI offer an apartment for rent in the very centre of Wrocław right next to Pl. Grunwaldzki, near to many companies and universities (PWr, UP, AM). Available from May. Full infrastructure in the neighbourhood. <br />\nThe apartment is located on the 2nd floor, 48 m2, consists of two rooms (large living room and bedroom), newly renovated kitchen, small bathroom and a hall. Fully furnished and equipped, ready to move - available immediately. <br />\n<br />\nPerfect for couple or 2+1. <br />\n<br />\nRent: 2900 PLN (3700 PLN with all fees, including gas, electricity, Internet and cable TV with UPC, water). <br />\nNote: possibility to negotiate a lower price for the months of May-September 2023. <br />\n<br />\nEnglish speaking owner.",
		"promotion": {
			"highlighted": True,
			"urgent": False,
			"top_ad": True,
			"options": [
				"bundle_optimum"
			],
			"b2c_ad_page": False,
			"premium_ad_page": False
		},
		"params": [
			{
				"key": "floor_select",
				"name": "Poziom",
				"type": "select",
				"value": {
					"key": "floor_2",
					"label": "2"
				}
			},
			{
				"key": "furniture",
				"name": "Umeblowane",
				"type": "select",
				"value": {
					"key": "yes",
					"label": "Tak"
				}
			},
			{
				"key": "price",
				"name": "Cena",
				"type": "price",
				"value": {
					"value": 2900,
					"type": "arranged",
					"arranged": True,
					"budget": False,
					"currency": "PLN",
					"negotiable": True,
					"converted_value": None,
					"previous_value": None,
					"converted_previous_value": None,
					"converted_currency": None,
					"label": "2 900 zł"
				}
			},
			{
				"key": "builttype",
				"name": "Rodzaj zabudowy",
				"type": "select",
				"value": {
					"key": "kamienica",
					"label": "Kamienica"
				}
			},
			{
				"key": "m",
				"name": "Powierzchnia",
				"type": "input",
				"value": {
					"key": "48",
					"label": "48 m²"
				}
			},
			{
				"key": "rooms",
				"name": "Liczba pokoi",
				"type": "select",
				"value": {
					"key": "two",
					"label": "2 pokoje"
				}
			},
			{
				"key": "rent",
				"name": "Czynsz (dodatkowo)",
				"type": "input",
				"value": {
					"key": "800",
					"label": "800 zł"
				}
			}
		],
		"key_params": [
			"m",
			"rooms"
		],
		"business": False,
		"user": {
			"id": 375191,
			"created": "2010-11-21T19:12:33+01:00",
			"other_ads_enabled": True,
			"name": "Joanna",
			"logo": None,
			"logo_ad_page": None,
			"social_network_account_type": "facebook",
			"photo": "https://img-resizer.prd.01.eu-west-1.eu.olx.org/img-eu-olxpl-production/549108904_1_100x100_rev022.jpg",
			"banner_mobile": "",
			"banner_desktop": "",
			"company_name": "",
			"about": "",
			"b2c_business_page": False,
			"is_online": False,
			"last_seen": "2023-05-16T10:19:44+02:00",
			"seller_type": None,
			"uuid": "dc0d9cc4-98e0-433b-b17c-e09a4d7b85c8"
		},
		"status": "active",
		"contact": {
			"name": "Joanna",
			"phone": True,
			"chat": True,
			"negotiation": True,
			"courier": False
		},
		"map": {
			"zoom": 13,
			"lat": 51.11464,
			"lon": 17.06436,
			"radius": 8,
			"show_detailed": False
		},
		"location": {
			"city": {
				"id": 19701,
				"name": "Wrocław",
				"normalized_name": "wroclaw"
			},
			"district": {
				"id": 387,
				"name": "Śródmieście"
			},
			"region": {
				"id": 3,
				"name": "Dolnośląskie",
				"normalized_name": "dolnoslaskie"
			}
		},
		"photos": [
			{
				"id": 5729769341,
				"filename": "ee1d1vfzs25z2-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/ee1d1vfzs25z2-PL/image;s={width}x{height}"
			},
			{
				"id": 2349043201,
				"filename": "t3di4bxyxg7l2-PL",
				"rotation": 0,
				"width": 933,
				"height": 700,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/t3di4bxyxg7l2-PL/image;s={width}x{height}"
			},
			{
				"id": 5729769342,
				"filename": "kklplv0kdsmv3-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/kklplv0kdsmv3-PL/image;s={width}x{height}"
			},
			{
				"id": 5729769343,
				"filename": "bcggfy04ggk6-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/bcggfy04ggk6-PL/image;s={width}x{height}"
			},
			{
				"id": 5729769344,
				"filename": "c5zaw8dtytck2-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/c5zaw8dtytck2-PL/image;s={width}x{height}"
			},
			{
				"id": 5729769345,
				"filename": "lo5tpctx4sog-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/lo5tpctx4sog-PL/image;s={width}x{height}"
			},
			{
				"id": 5729769346,
				"filename": "2jj8z0sa7ic01-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/2jj8z0sa7ic01-PL/image;s={width}x{height}"
			},
			{
				"id": 5729769347,
				"filename": "3uffcgm8iorz1-PL",
				"rotation": 0,
				"width": 3468,
				"height": 4624,
				"link": "https://ireland.apollo.olxcdn.com:443/v1/files/3uffcgm8iorz1-PL/image;s={width}x{height}"
			}
		],
		"partner": None,
		"category": {
			"id": 15,
			"type": "real_estate"
		},
		"delivery": {
			"rock": {
				"offer_id": None,
				"active": False,
				"mode": "NotEligible"
			}
		},
		"safedeal": {
			"weight": 0,
			"weight_grams": 0,
			"status": "unactive",
			"safedeal_blocked": False,
			"allowed_quantity": []
		},
		"shop": {
			"subdomain": None
		},
		"offer_type": "offer"
	}