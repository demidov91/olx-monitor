from olx_monitor.updater import build_basic_message


def test_build_basic_message(olx_offer):
    actual = build_basic_message(olx_offer)
    assert actual == """*Reklama
2 pokoje - Plac Grunwaldzki - od zaraz - promocja V-IX 2023!

2 900 zł + 800 zł
48 m², 2 pokoje
Wrocław, Śródmieście

https://www.olx.pl/d/oferta/2-pokoje-plac-grunwaldzki-od-zaraz-promocja-v-ix-2023-CID3-IDIiUR2.html"""
