# import sys
# import os
# sys.path.append(os.path.abspath("."))
# print(sys.path)
from prediction.models import PRED_data, STORE_data, CUSTOMER_data
from prediction.ml import corona_tokyo_learning, create_dfpredict, drop_make_df, people_flow_learning
from django.core.management.base import BaseCommand
import os
from devtools import debug
from selenium import webdriver
import time
import random
import requests
import datetime
from dateutil.relativedelta import relativedelta
import jpholiday
import pandas as pd

from dotenv import load_dotenv
load_dotenv()


# if os.getenv("TZ") == 'Asia/Tokyo':
#     to_day = datetime.datetime.now().date() - relativedelta(days=1)
# else:  # heroku上の時間に注意
#     to_day = datetime.datetime.now() + relativedelta(hours=9) - relativedelta(days=1)
#     to_day = to_day.date()
year = input('year? if no input, use current: ')
if year:
    year = int(year)
else:
    year = datetime.datetime.now().year

month = input('month? if no input, use current: ')
if month:
    month = int(month)
else:
    month = datetime.datetime.now().month

day = int(input('day?: '))

to_day = datetime.date(year, month, day)


fes_key = os.environ["UBIREGI_FES_KEY"]
garage_key = os.environ["UBIREGI_GARAGE_KEY"]
tourou_key = os.environ["UBIREGI_TOUROU_KEY"]
wanaichi_key = os.environ["UBIREGI_WANAICHI_KEY"]
wananakame_key = os.environ["UBIREGI_WANANAKAME_KEY"]
keydict = {"fes": fes_key, "garage": garage_key, "tourou": tourou_key, "wanaichi": wanaichi_key, "wananakame": wananakame_key}
# keydict = {"fes": fes_key}


def get_weather(to_day):
    date = datetime.date.strftime(to_day, "%Y%m%d")
    year = date[:4]
    month = date[4:6]
    day = date[6:]

    user_agent = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    ]
    options = webdriver.ChromeOptions()
    # if os.getenv('GOOGLE_CHROME_SHIM'):
    #     options.binary_location = os.getenv('GOOGLE_CHROME_SHIM')
    now_ua = user_agent[random.randrange(0, len(user_agent), 1)]
    options.add_argument('--user-agent=' + now_ua)
    options.add_argument('--disable-desktop-notifications')
    options.add_argument("--disable-extensions")
    options.add_argument('--lang=ja')
    options.add_argument('--blink-settings=imagesEnabled=false')  # 画像なし
    options.add_argument('--no-sandbox')
    # options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
    options.add_argument('--proxy-server="direct://"')  # Proxy経由ではなく直接接続する
    # if chrome_binary_path:
    #     options.binary_location = chrome_binary_path
    options.add_argument('--single-process')
    options.add_argument('--disable-application-cache')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--start-maximized')

    options.add_argument('--headless')  # ヘッドレス
    options.add_argument('--disable-gpu')  # 不要？?
    # options.page_load_strategy = 'none'

    driver = webdriver.Chrome('chromedriver', options=options)

    # https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=45&block_no=47682&year=2021&month=3&day=2&view=
    # https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=44&block_no=47662&year=2021&month=03&day=2&view=
    url_dict = {
        "chiba": f"https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=45&block_no=47682&year={year}&month={month}&day={day}&view=",
        "tokyo": f"https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=44&block_no=47662&year={year}&month={month}&day={day}&view="
    }

    for locale, url in url_dict.items():
        try:
            df_wthr = pd.read_html(url)[0]
            print(f'get {locale} page_source')

            df_wthr = df_wthr.T.reset_index(level=0, drop=True).T
            df_wthr_l = df_wthr.query("11 <= 時 <= 15")
            df_wthr_d = df_wthr.query("17 <= 時 <= 20")

            result_tempe_l = df_wthr_l.loc[:, "気温(℃)"].mean()

            if len(df_wthr_l[df_wthr_l["降水量(mm)"] != "--"]) == 0:
                result_rain_l = 0
            elif len(df_wthr_l[df_wthr_l["降水量(mm)"] != "--"]) == 1:
                result_rain_l = df_wthr_l[df_wthr_l["降水量(mm)"] != "--"]["降水量(mm)"].astype('float').values[0]
            else:
                result_rain_l = df_wthr_l[df_wthr_l["降水量(mm)"] != "--"]["降水量(mm)"].astype('float').mean()

            result_tempe_d = df_wthr_d.loc[:, "気温(℃)"].mean()

            if len(df_wthr_d[df_wthr_d["降水量(mm)"] != "--"]) == 0:
                result_rain_d = 0
            elif len(df_wthr_d[df_wthr_d["降水量(mm)"] != "--"]) == 1:
                result_rain_d = df_wthr_d[df_wthr_d["降水量(mm)"] != "--"]["降水量(mm)"].astype('float').values[0]
            else:
                result_rain_d = df_wthr_d[df_wthr_d["降水量(mm)"] != "--"]["降水量(mm)"].astype('float').mean()
            print('get weather OK')
        except Exception:
            print('昨日の天気データの取得に失敗しました。0を入力します')
            result_rain_l = None
            result_tempe_l = None
            result_rain_d = None
            result_tempe_d = None

        if locale == "chiba":
            chiba_rain_l, chiba_tempe_l, chiba_rain_d, chiba_tempe_d = result_rain_l, result_tempe_l, result_rain_d, result_tempe_d
        elif locale == "tokyo":
            tokyo_rain_l, tokyo_tempe_l, tokyo_rain_d, tokyo_tempe_d = result_rain_l, result_tempe_l, result_rain_d, result_tempe_d

    # ここから予報取得ーーーーーーーーーーー
    fore_url_dict = {
        "chiba": "https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code=1220400",
        "tokyo": "https://www.jma.go.jp/bosai/forecast/#area_type=class20s&area_code=1310200",
    }
    for locale, url in fore_url_dict.items():
        try:
            driver.get(url)
            time.sleep(4)
            df_fore = pd.read_html(driver.page_source)

            df_fore_weekly = df_fore[5]

            def trans_rain_chance(rain_chance):
                if rain_chance <= 20:
                    volume = 0
                elif 20 < rain_chance <= 50:
                    volume = 1
                else:
                    volume = 2
                return volume

            weekly_rain_list = list(df_fore_weekly.loc[3, 3:9])
            tomorrow = [int(i) for i in weekly_rain_list[0].split('/')]
            weekly_rain_list[0] = [sum(tomorrow[:2]) / 2, sum(tomorrow[2:]) / 2]
            # type [[,], , , , , , ]
            weekly_rain_list[0] = [trans_rain_chance(int(v)) for v in weekly_rain_list[0]]
            weekly_rain_list[1:] = [trans_rain_chance(int(v)) for v in weekly_rain_list[1:]]

            max = [int(i.split('(')[0]) for i in list(df_fore_weekly.loc[5, 3:9])]  # 元データex→'9(7～10)'
            min = [int(i.split('(')[0]) for i in list(df_fore_weekly.loc[6, 3:9])]
            temp_list = []
            for i in range(len(max)):  # 最高気温と最低気温の差の中間25％
                difference = (max[i] - min[i]) * 0.25
                temp_list.append([max[i] - difference, min[i] + difference])
            # type [[,],[,],[,],[,],[,],[,],[,]]
            print(f'get {locale} forecast OK')

        except Exception as e:
            print(e)
            print('天気予報データの取得に失敗しました。移動平均を入力します')

            PRED_data.objects.all().filter()

            weekly_rain_list = None
            temp_list = None
        if locale == "chiba":
            chiba_rain_list, chiba_tempe_list = weekly_rain_list, temp_list
        elif locale == "tokyo":
            tokyo_rain_list, tokyo_tempe_list = weekly_rain_list, temp_list

    driver.quit()
    return chiba_rain_l, chiba_tempe_l, chiba_rain_d, chiba_tempe_d, tokyo_rain_l, tokyo_tempe_l, tokyo_rain_d, tokyo_tempe_d, chiba_rain_list, chiba_tempe_list, tokyo_rain_list, tokyo_tempe_list


def get_corona_tokyo(to_day):
    endpoint = "https://api.data.metro.tokyo.lg.jp/v1/Covid19Patient"
    param = {
        "from": str(to_day),
        "till": str(to_day),
        "limit": 1000,  # 最大1000
    }
    res = requests.get(endpoint, params=param).json()
    result = len(res[0])

    while not res[1]["moreResults"] == "NO_MORE_RESULTS":
        print('Go_next_result')
        param = {
            "from": str(to_day),
            "till": str(to_day),
            "limit": 1000,  # 最大1000
            "cursor": res[1]["endCursor"],
        }
        res = requests.get(endpoint, params=param).json()
        result += len(res[0])

    print('Get_corona')

    return result


def get_corona_pred(to_day):
    df = create_dfpredict(for_peopleflow=True)
    latest_df = df[df.index == to_day]
    latest_df, _ = drop_make_df(latest_df, "corona_tokyo")
    model = corona_tokyo_learning(to_day)
    # debug(latest_df,to_day)
    pred = model.predict(latest_df)
    print('corona predict OK')
    return pred[0]


def get_people_flow_predict(to_day):
    df = create_dfpredict(for_peopleflow=True)
    latest_df = df[df.index == to_day]

    latest_df, _ = drop_make_df(latest_df, "people")
    model = people_flow_learning(to_day)
    # debug(latest_df,to_day)
    pred = model.predict(latest_df)
    print('peopleflow predict OK')
    return pred[0]


def get_customer_count(APIkey, to_day):
    query = "accounts/current/checkouts/close"
    API_Endpoint = "https://ubiregi.com/api/3/{}".format(query)
    headers = {"X-Ubiregi-Auth-Token": APIkey, "Content-Type": "application/json"}

    today = f"{to_day}T04:00:00+09:00"
    now = f"{to_day + relativedelta(days=1)}T17:00:00+09:00"

    params = {
        "since": f"{today}",
        "until": f"{now}",
        "total_count": "true",
    }
    res = requests.get(API_Endpoint, headers=headers, params=params).json()

    customer_lunch = 0
    customer_dinner = 0
    price_lunch = 0
    price_dinner = 0

    def translate_iso(time: str):
        startTime = datetime.datetime.fromisoformat(time + 'T09:00:00' + '+09:00')
        fivePM = datetime.datetime.fromisoformat(time + 'T17:00:00' + '+09:00')
        endTime = datetime.datetime.fromisoformat(time + 'T06:00:00' + '+09:00') + relativedelta(days=1)
        return startTime, fivePM, endTime

    next_flg = True
    while next_flg is True:
        startTime, fivePM, endTime = translate_iso(str(to_day))
        for s in res["checkouts"]:
            if startTime <= datetime.datetime.fromisoformat(s["paid_at"].replace('Z', '+00:00')) < fivePM:
                if s["status"] == "close":
                    customer_lunch += s["customers_count"]
                    price_lunch += round(float(s["price"]))
            elif fivePM <= datetime.datetime.fromisoformat(s["paid_at"].replace('Z', '+00:00')) <= endTime:
                if s["status"] == "close":
                    customer_dinner += s["customers_count"]
                    price_dinner += round(float(s["price"]))
        if res["next-url"]:
            next_url = res["next-url"]
            res = requests.get(next_url, headers=headers).json()
            print("get_next!!")
        else:
            next_flg = False

    print('Get_ubiregi')
    return customer_lunch, customer_dinner, price_lunch, price_dinner


def prepro(to_day):
    # 曜日変換ーーーーーー
    week_num = to_day.weekday()
    week_str = "月" if week_num == 0 else "火" if week_num == 1 else "水" if week_num == 2 else "木" if week_num == 3 else "金" if week_num == 4 else "土" if week_num == 5 else "日"

    # 休日フラグーーーーーー
    before_holiday_flg = 1 if jpholiday.is_holiday(to_day + relativedelta(days=1)) else 0
    holiday_flg = 1 if jpholiday.is_holiday(to_day) else 0

    if to_day <= datetime.date(2021, 3, 21):  # 3/7まではtrue
        emergency_flg = 1
    else:
        emergency_flg = 0

    # 時短フラグーーーーーーーー
    if to_day <= datetime.date(2021, 9, 12):  # 3/7まではtrue
        shorttime_at20_flg = 1
    else:
        shorttime_at20_flg = 0
    return week_str, before_holiday_flg, holiday_flg, emergency_flg, shorttime_at20_flg


def insert_db_pred_data(to_day):
    print(datetime.datetime.now())
    print(to_day)

    # 天気取得ーーーーーーーー
    rain_chiba_l, tempe_chiba_l, rain_chiba_d, tempe_chiba_d, rain_tokyo_l, tempe_tokyo_l, rain_tokyo_d, tempe_tokyo_d, rain_chiba_list, tempe_chiba_list, rain_tokyo_list, tempe_tokyo_list = get_weather(to_day)
    # コロナ感染数ーーーーーー
    corona = get_corona_tokyo(to_day)

    # 当日ーーーーーーーーー
    wthr_data_dict = {"chiba": rain_chiba_l, "tokyo": rain_tokyo_l}
    for locale, data in wthr_data_dict.items():
        if data is None:
            before5days = to_day - relativedelta(days=5)
            before1days = to_day - relativedelta(days=1)
            obj = PRED_data.objects.filter(date__gte=before5days, date__lte=before1days)
            rain_l_list, tempe_l_list, rain_d_list, tempe_d_list = [], [], [], []
            if locale == "chiba":
                for o in obj:
                    rain_l_list.append(o.rain_l)
                    tempe_l_list.append(o.tempe_l)
                    rain_d_list.append(o.rain_d)
                    tempe_d_list.append(o.tempe_d)
                rain_chiba_l = sum(rain_l_list) / len(rain_l_list)
                tempe_chiba_l = sum(tempe_l_list) / len(tempe_l_list)
                rain_chiba_d = sum(rain_d_list) / len(rain_d_list)
                tempe_chiba_d = sum(tempe_d_list) / len(tempe_d_list)
            elif locale == "tokyo":
                for o in obj:
                    rain_l_list.append(o.rain_tokyo_l)
                    tempe_l_list.append(o.tempe_tokyo_l)
                    rain_d_list.append(o.rain_tokyo_d)
                    tempe_d_list.append(o.tempe_tokyo_d)
                rain_tokyo_l = sum(rain_l_list) / len(rain_l_list)
                tempe_tokyo_l = sum(tempe_l_list) / len(tempe_l_list)
                rain_tokyo_d = sum(rain_d_list) / len(rain_d_list)
                tempe_tokyo_d = sum(tempe_d_list) / len(tempe_d_list)

    week_str, before_holiday_flg, holiday_flg, emergency_flg, shorttime_at20_flg = prepro(to_day)
    debug(week_str, before_holiday_flg, holiday_flg, rain_chiba_l, tempe_chiba_l, rain_chiba_d, tempe_chiba_d, rain_tokyo_l, tempe_tokyo_l, rain_tokyo_d, tempe_tokyo_d, corona, emergency_flg, shorttime_at20_flg)
    PRED_data.objects.update_or_create(
        date=to_day,
        defaults={
            "week": week_str,
            "before_holiday": before_holiday_flg,
            "holiday": holiday_flg,
            "rain_l": rain_chiba_l,
            "tempe_l": tempe_chiba_l,
            "rain_d": rain_chiba_d,
            "tempe_d": tempe_chiba_d,
            "rain_tokyo_l": rain_tokyo_l,
            "tempe_tokyo_l": tempe_tokyo_l,
            "rain_tokyo_d": rain_tokyo_d,
            "tempe_tokyo_d": tempe_tokyo_d,
            "corona_tokyo": corona,
            # "peopleflow_shibuya": ,
            "state_of_emergency": emergency_flg,
            "shorttime_at22": 0,
            "shorttime_at20": shorttime_at20_flg,
        })

    # 翌日以降ーーーーーーーーー
    # for i in range(9):
    for i in range(45):
        to_day += relativedelta(days=1)

        before5days = to_day - relativedelta(days=5)
        before1days = to_day - relativedelta(days=1)
        ma_obj = PRED_data.objects.filter(date__gte=before5days, date__lte=before1days)
        # コロナ移動平均ーーーーーー
        # corona_list = []
        # for o in ma_obj:
        #     corona_list.append(o.corona_tokyo)
        # corona = sum(corona_list) / len(corona_list)

        # 天気情報処理ーーーーーー
        wthr_list_dict = {
            "chiba": [rain_chiba_list, tempe_chiba_list],
            "tokyo": [rain_tokyo_list, tempe_tokyo_list],
        }
        for locale, datalist in wthr_list_dict.items():
            weekly_rain_list = datalist[0]
            tempe_list = datalist[1]

            try:
                if type(weekly_rain_list[i]) == list:
                    rain_l = weekly_rain_list[i][0]
                    rain_d = weekly_rain_list[i][-1]
                else:
                    rain_l = weekly_rain_list[i]
                    rain_d = weekly_rain_list[i]
            except Exception:
                rain_l = 0
                rain_d = 0
            try:
                tempe_l = tempe_list[i][0]
                tempe_d = tempe_list[i][-1]
            except Exception:  # 移動平均取得ーーーーー
                tempe_l_list, tempe_d_list = [], []
                for o in ma_obj:
                    tempe_l_list.append(o.tempe_l)
                    tempe_d_list.append(o.tempe_d)
                tempe_l = sum(tempe_l_list) / len(tempe_l_list)
                tempe_d = sum(tempe_d_list) / len(tempe_d_list)

            if locale == "chiba":
                rain_c_l, rain_c_d, tempe_c_l, tempe_c_d = rain_l, rain_d, tempe_l, tempe_d
            elif locale == "tokyo":
                rain_t_l, rain_t_d, tempe_t_l, tempe_t_d = rain_l, rain_d, tempe_l, tempe_d

        # その他データ取得ーーーーー
        week_str, before_holiday_flg, holiday_flg, emergency_flg, shorttime_at20_flg = prepro(to_day)

        # debug(week_str, before_holiday_flg, holiday_flg, rain_c_l, tempe_c_l, rain_c_d, tempe_c_d, rain_t_l, tempe_t_l, rain_t_d, tempe_t_d, emergency_flg, shorttime_at20_flg,)

        PRED_data.objects.update_or_create(
            date=to_day,
            defaults={
                "week": week_str,
                "before_holiday": before_holiday_flg,
                "holiday": holiday_flg,
                "rain_l": rain_c_l,
                "tempe_l": tempe_c_l,
                "rain_d": rain_c_d,
                "tempe_d": tempe_c_d,
                "rain_tokyo_l": rain_t_l,
                "tempe_tokyo_l": tempe_t_l,
                "rain_tokyo_d": rain_t_d,
                "tempe_tokyo_d": tempe_t_d,
                # "corona_tokyo": corona,
                "state_of_emergency": emergency_flg,
                "shorttime_at22": 0,
                "shorttime_at20": shorttime_at20_flg,
            })

        corona = get_corona_pred(to_day)
        PRED_data.objects.update_or_create(
            date=to_day,
            defaults={
                "corona_tokyo": corona,
            })

        people_flow = get_people_flow_predict(to_day)
        # latest_date = PRED_data.objects.latest('date').date
        PRED_data.objects.update_or_create(
            date=to_day,
            defaults={
                "peopleflow_shibuya": people_flow,
            })

    print('DB insert OK')


def insert_db_customer_and_price(APIkey, to_day, store_name):
    # 客数取得ーーーーーー
    customer_lunch, customer_dinner, price_lunch, price_dinner = get_customer_count(APIkey, to_day)
    store = STORE_data.objects.get(store_name=store_name)
    week_str, _, _, _, _ = prepro(to_day)
    CUSTOMER_data.objects.update_or_create(
        date=to_day, store=store,
        defaults={
            "week": week_str,
            "cust_l": customer_lunch,
            "cust_d": customer_dinner,
            "price_l": price_lunch,
            "price_d": price_dinner,
        })
    print(store_name, customer_lunch, customer_dinner)


class Command(BaseCommand):  # コマンド python manage.py get_data_db
    def handle(self, *args, **options):

        flg = input('一日分？ →1  昨日までまとめて？ →0 : ')
        if flg == "1":
            st_day = to_day
            # st_day = datetime.date(2021,4,7)  # 一気に取得用
            while st_day <= to_day:
                insert_db_pred_data(st_day)
                print(st_day)
                for store_name, APIkey in keydict.items():
                    print(store_name)
                    insert_db_customer_and_price(APIkey, st_day, store_name)
                st_day += relativedelta(days=1)
            # # return super().handle(*args, **options)

        elif flg == "0":
            st_day = to_day
            last_day = datetime.datetime.now().date() - relativedelta(days=1)
            # st_day = datetime.date(2021,4,7)  # 一気に取得用
            while st_day <= last_day:
                print(f'last day {last_day}')
                insert_db_pred_data(st_day)
                print(st_day)
                for store_name, APIkey in keydict.items():
                    print(store_name)
                    insert_db_customer_and_price(APIkey, st_day, store_name)
                st_day += relativedelta(days=1)
            # # return super().handle(*args, **options)
