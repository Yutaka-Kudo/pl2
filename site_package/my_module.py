import os
from upload_part.models import PL_data, FoodCosts, DrinkCosts, LaborCosts, UtilityCosts_ComunicationCosts, AdvertisingCosts, OtherCosts, TaxExemptExpenses
from prediction.models import PRED_data, CUSTOMER_data  # 必要！

import datetime


def translate_storename(name: str, to_ja: bool = False):
    if to_ja:
        return 'FES' if name == 'fes' else 'Garage あそび' if name == 'garage' else '灯篭' if name == 'tourou' else '罠一目' if name == 'wanaichi' else '罠中目黒' if name == 'wananakame' else ''
    else:
        return 'fes' if name == 'FES' else 'Garage あそび' if name == 'garage' else 'tourou' if name == '灯篭' else 'wanaichi' if name == '罠一目' else 'wananakame' if name == '罠中目黒' else ''


fes_l = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー", "降水量:ディナー", "気温:ディナー", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
fes_d = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー", "降水量:ランチ", "気温:ランチ", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
garage_l = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
            "気温:ランチ", "降水量:ディナー", "気温:ディナー", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
garage_d = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
            "降水量:ランチ", "降水量:ディナー", "気温:ランチ", "気温:ディナー", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
tourou_l = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
            "気温:ランチ", "降水量:ディナー", "気温:ディナー", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
tourou_d = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
            "降水量:ランチ", "気温:ランチ", "気温:ディナー", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
wanaichi_l = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
              "気温:ランチ", "降水量:ディナー", "気温:ディナー", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
wanaichi_d = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
              "降水量:ランチ", "気温:ランチ", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
wananakame_l = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
                "気温:ランチ", "降水量:ディナー", "気温:ディナー", "降水量東京:ディナー", "気温東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
wananakame_d = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー",
                "降水量:ランチ", "気温:ランチ", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "時短22時", '来客数:ランチ', '来客数:ディナー']
corona_tokyo = ["曜日", "コロナ感染発表数:都内", "人流変化:渋谷", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー", "気温:ランチ", "降水量:ランチ", "降水量:ディナー", "降水量東京:ランチ", "降水量東京:ディナー", "気温東京:ランチ", "気温東京:ディナー"]

# people = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー", "人流変化:渋谷", "時短22時", "時短20時", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー"]
people = ["曜日", "天気:ランチ", "天気:ディナー", "風速:ランチ", "風速:ディナー", "人流変化:渋谷", "時短22時", "降水量東京:ランチ", "気温東京:ランチ", "降水量東京:ディナー", "気温東京:ディナー"]


drop_list = {
    "fes_l": fes_l, "fes_d": fes_d,
    "garage_l": garage_l, "garage_d": garage_d,
    "tourou_l": tourou_l, "tourou_d": tourou_d,
    "wanaichi_l": wanaichi_l, "wanaichi_d": wanaichi_d,
    "wananakame_l": wananakame_l, "wananakame_d": wananakame_d,
    "corona_tokyo": corona_tokyo,
    "people": people,
}


def trans_date(str: str = "", date: datetime.date = None):
    """YYYY-mm-ddの形"""
    if str:
        result = datetime.datetime.strptime(str, '%Y-%m-%d').date()
    elif date:
        result = datetime.date.strftime(date, '%Y-%m-%d')
    else:
        result = None
        raise TypeError(f'引数はstrかdateにしましょう。{type(str if str else date)}')
    return result


# 全角、半角 変換テーブルーーーーーーーーーーーーー
ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))
ZEN2HAN = str.maketrans(ZEN, HAN)
# ーーーーーーーーーーーーーーーーーーーーーーー

# あるやつは、モデル名.属性.field.verbose_name にある。
def create_fieldname_dict(dbmodel):
    ver_name_list = []
    db_column_list = []
    for attr in dir(dbmodel):
        attribute = getattr(dbmodel, f"{attr}")
        field = getattr(attribute, "field", None)
        ver_name = getattr(field, "verbose_name", None)
        if ver_name:
            ver_name_list.append(ver_name)
            db_column_list.append(attr)

        # try: # execは危ないので極力使わない
        #     exec(f"ver_name_list.append({dbmodel.__name__}.{attr}.field.verbose_name)")
        #     db_column_list.append(attr)
        # except Exception:
        #     pass
    return dict(zip(db_column_list, ver_name_list))


pl_dbdict = {}
for dbmodel in [PL_data, FoodCosts, DrinkCosts, LaborCosts, UtilityCosts_ComunicationCosts, AdvertisingCosts, OtherCosts, TaxExemptExpenses]:
    pl_dbdict[dbmodel] = create_fieldname_dict(dbmodel)


end_dir = {
    "close": "https://ubiregi.com/api/3/accounts/current/checkouts/close",
    "items": "https://ubiregi.com/api/3/menus/menu_id/items",  # menu_idを置き換える
    "accounts": "https://ubiregi.com/api/3/accounts/current",
}


def create_logger(name, set_level: str = 'debug'):
    import logging

    from logging import getLogger, StreamHandler, DEBUG, Formatter

    if not set_level:
        logging.disable(logging.DEBUG)

    # logger = getLogger(__name__)
    logger = getLogger(name)
    handler = StreamHandler()
    handler.setLevel(logging.getLevelName(set_level.upper()))
    handler.setFormatter(Formatter("%(asctime)s %(name)s:%(lineno)s %(funcName)s \033[33m[%(levelname)s]\033[0m: %(message)s"))
    logger.setLevel(logging.getLevelName(set_level.upper()))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
