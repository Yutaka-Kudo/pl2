from icecream import ic
import requests
import datetime
from dateutil.relativedelta import relativedelta
import openpyxl
import copy
import os
from pprint import pprint as pp
from devtools import debug

from dotenv import load_dotenv
load_dotenv()

ic.configureOutput(prefix='', includeContext=True)
# ic.disable()

# 標準インデックスパラメータ  since, until, glb, limit.verbose = true, image = blob, total_count = true


class Accounts:
    def __init__(self, store_name):
        self.url_query = "accounts/current"
        self.API_Endpoint = f"https://ubiregi.com/api/3/{self.url_query}"
        API_Key = os.environ[f'UBIREGI_{store_name.upper()}_KEY']
        self.headers = {"X-Ubiregi-Auth-Token": API_Key, "Content-Type": "application/json"}
        self.params = {"total_count": "true"}
        self.res = None

    def get_apiResponse(self):
        res = requests.get(self.API_Endpoint, headers=self.headers, params=self.params)
        ic(res.status_code)
        self.res = res.json()
        return self.res

    @property
    def find_dict_keys(self):  # 辞書キー探し
        print("キー: "+str([k for k in self.res.keys()]))

    def count(self, dict_key):  # 総数
        counts = len(self.res["{}".format(dict_key)])
        print("オブジェクト数: " + str(counts))
        return counts

    def show_menuId(self):
        self.res = self.res or self.get_apiResponse()
        ic(self.res['account']['menus'])

    def show_customerTags(self):
        self.res = self.res or self.get_apiResponse()
        ic(self.res['account']['customer_tags'])

    def show_paymentTypes(self):
        self.res = self.res or self.get_apiResponse()
        ic(self.res['account']['payment_types'])


class Sales(Accounts):
    all_ids = {
        'fes': {
            'media': {
                "free": 54904,
                "gaihan": 0,
                "hp": 54905,
                "gn": 54906,
                "tb": 54908,
                "retty": 54907,
            },
            'pay_type': {
                'credit': 125252,
                'paypay': 164964,
                'rakutenpay': 181659,
                'melpay_dbarai': 181660,
                'aupay': 181662,
                'gn_point': 181665,
                'hp_point': 181663,
                'hpticket': 0,
                'tb_point': 181664,
                'uber': 171247,
                'demaekan': 172802,
                'foodpanda': 0,
                'goto': 179038,
                'other': 0,
                'cash': 125251,
            }
        },
        'garage': {
            'media': {
                "free": 47323,
                "gaihan": 0,
                "hp": 47321,
                "gn": 47320,
                "tb": 47322,
                "retty": 0,
            },
            'pay_type': {
                'credit': 112746,
                'paypay': 165327,
                'rakutenpay': 127415,
                'melpay_dbarai': 179817,
                'aupay': 181274,
                'gn_point': 181898,
                'hp_point': 181896,
                'hpticket': 113285,
                'tb_point': 181897,
                'uber': 171390,
                'demaekan': 0,
                'foodpanda': 0,
                'goto': 179816,
                'other': 0,
                'cash': 112745,
            }
        },
        'tourou': {
            'media': {
                "free": 0,
                "gaihan": 1,
                "hp": 1,
                "gn": 1,
                "tb": 1,
                "retty": 1,
            },
            'pay_type': {
                'credit': 150409,
                'paypay': 166411,
                'rakutenpay': 0,
                'melpay_dbarai': 181899,
                'aupay': 181900,
                'gn_point': 181901,
                'hp_point': 150410,
                'hpticket': 0,
                'tb_point': 181902,
                'uber': 0,
                'demaekan': 0,
                'foodpanda': 0,
                'goto': 180233,
                'other': 0,
                'cash': 150408,
            }
        },
        'wanaichi': {
            'media': {
                'free': 65445,
                "gaihan": 0,
                'hp': 65447,
                'gn': 65450,
                'tb': 65448,
                "retty": 0,
            },
            'pay_type': {
                'credit': 151256,
                'paypay': 165434,
                'rakutenpay': 151257,
                'melpay_dbarai': 180661,
                'aupay': 181669,
                'gn_point': 0,
                'hp_point': 181672,  # ポイント系が分かれてないのでhpポイントにまとめてる
                'hpticket': 0,
                'tb_point': 0,
                'uber': 181670,
                'demaekan': 0,
                'foodpanda': 0,
                'goto': 181671,
                'other': 0,
                'cash': 151255,
            }
        },
        'wananakame': {
            'media': {
                "free": 75214,
                "gaihan": 0,
                "hp": 75216,
                "gn": 75217,
                "tb": 75215,
                "retty": 0,
            },
            'pay_type': {
                'credit': 176946,
                'paypay': 177872,
                'rakutenpay': 0,
                'melpay_dbarai': 177876,
                'aupay': 177877,
                'gn_point': 0,
                'hp_point': 0,
                'hpticket': 0,
                'tb_point': 0,
                'uber': 0,
                'demaekan': 0,
                'foodpanda': 0,
                'goto': 0,
                'other': 176947,
                'cash': 176945,
            }
        },
    }

    def __init__(self, store_name, to_day):
        super().__init__(store_name)
        self.url_query = "accounts/current/checkouts/close"
        self.API_Endpoint = f"https://ubiregi.com/api/3/{self.url_query}"

        JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")

        self.today = to_day+relativedelta(hours=6)
        self.today_iso = datetime.datetime.isoformat(self.today, timespec="seconds") + '+09:00'

        self.until = self.today+relativedelta(days=1)
        # self.until_iso = datetime.datetime.now().astimezone(JST)
        self.until_iso = datetime.datetime.isoformat(self.until, timespec="seconds") + '+09:00'

        self.params = {"since": f"{self.today_iso}",
                       "until": f"{self.until_iso}",
                       "total_count": "true"
                       }

        self.ids = self.all_ids[store_name]

        self.res = None

    def get_apiResponse(self):  # オーバーライド
        self.res = requests.get(self.API_Endpoint, headers=self.headers, params=self.params).json()
        # Close以外除外
        self.fill_in_the_blanks_with_FREE(self.res)
        self.remove_other_than_CLOSE(self.res)
        return self.res

    def fill_in_the_blanks_with_FREE(self, res):
        for s in res["checkouts"]:
            s["customer_tag_ids"]
            if not s["customer_tag_ids"]:
                s["customer_tag_ids"].append(self.ids['media']['free'])
        return res

    def remove_other_than_CLOSE(self, res):
        for s in res["checkouts"][:]:
            if s["status"] != "close":
                res["checkouts"].remove(s)
        return res

    @property
    def find_customer_tag_ids(self):
        self.res = self.res or self.get_apiResponse()
        for s in self.res["checkouts"]:
            print(s["customer_tag_ids"])

    def timesearch_by_customer_tag(self, tag_ids):  # 媒体タグから会計時間を出す
        self.res = self.res or self.get_apiResponse()
        fff = self.today_iso.replace(self.today_iso[11:19], "17:00:00")
        fff = datetime.datetime.fromisoformat(fff)
        for s in self.res["checkouts"]:
            if s["customer_tag_ids"] == [tag_ids]:
                fix_time = datetime.datetime.fromisoformat(
                    s["paid_at"].replace("Z", "+00:00"))
                if fix_time < fff:
                    print('lunch')
                    print(fix_time)
                else:
                    print('dinner')
                    print(fix_time)

    def detection_customer_tag(self, *args):  # タグ検出
        self.res = self.res or self.get_apiResponse()
        res_list = self.res["checkouts"]
        for s in res_list:
            sl = s["customer_tag_ids"][:]
            for i in range(len(args)):
                try:
                    if sl[-1] == args[i]:
                        sl.clear()
                except Exception:
                    pass
            try:
                if sl[0]:
                    print(sl)
            except Exception:
                pass
