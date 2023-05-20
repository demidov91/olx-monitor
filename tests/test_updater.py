from olx_monitor.updater import build_basic_message


def test_build_basic_message__generic(olx_offer_generic):
    actual = build_basic_message(olx_offer_generic)
    assert actual == """*Reklama
2 pokoje - Plac Grunwaldzki - od zaraz - promocja V-IX 2023!

2 900 zł + 800 zł
48 m², 2 pokoje
Wrocław, Śródmieście

https://www.olx.pl/d/oferta/2-pokoje-plac-grunwaldzki-od-zaraz-promocja-v-ix-2023-CID3-IDIiUR2.html"""


def test_build_basic_message__wanna(olx_offer_wanna):
    actual = build_basic_message(olx_offer_wanna)
    assert actual == """*Reklama
wyjątkowe-2pok-62m2-Sępolno-balkon-ogród-lux

3 800 zł + 480 zł
62 m², 2 pokoje, 🛁
Wrocław, Śródmieście

https://www.olx.pl/d/oferta/wyjatkowe-2pok-62m2-sepolno-balkon-ogrod-lux-CID3-IDPCEK4.html"""
