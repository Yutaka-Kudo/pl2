# from pprint import pprint as pp
import datetime
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os
from dotenv import load_dotenv
load_dotenv()

line_api_key = os.environ["LineBotApiKey"]
line_bot_api = LineBotApi(line_api_key)
# WebhookHandlerKey = os.environ["WebhookHandlerKey"]
# handler= WebhookHandler('WebhookHandlerKey')

line_bot_list = []

now = datetime.datetime.now()
JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")


def notify_todays_illegal():
    checker_for_bot()
    print("start notifications")
    print(line_bot_list)
    if line_bot_list:
        text = ""
        for i in [u for u in range(len(line_bot_list)) if u % 3 == 0]:
            text += f"本日、{line_bot_list[i]} で\n{line_bot_list[i+1]} に\n『{line_bot_list[i+2]}』の処理が行われました。\n"
        messages = TextSendMessage(text=text)
        line_bot_api.broadcast(messages=messages, notification_disabled=True)


def checker_for_bot():
    def convert_str_to_datetime_jst(str_time: str):
        paid_at = str(datetime.datetime.fromisoformat(str_time.replace("Z", "+00:00")).astimezone(JST))[:19]  # ex. 2021-01-02 19:51:40
        paid_at = paid_at.split('-')  # ex. [2021, 01, 02 19:51:40]
        paid_at[0] += "年"
        paid_at[1] += "月"
        paid_at = "".join(paid_at).replace(' ', '日 ')
        return paid_at

    def translate_status_to_japanese(status_msg: str):
        if status_msg == "close":
            status = "会計済み"
            return status
        elif status_msg == "delete":
            status = "中断"
            return status
        elif status_msg == "cancel":
            status = "取り消し"
            return status

    fes_key = os.environ["UBIREGI_FES_KEY"]
    garage_key = os.environ["UBIREGI_GARAGE_KEY"]
    tourou_key = os.environ["UBIREGI_TOUROU_KEY"]
    ichi_key = os.environ["UBIREGI_ICHI_KEY"]
    nakame_key = os.environ["UBIREGI_NAKAME_KEY"]
    api_key_dic = {
        "FES": fes_key,
        "Garage": garage_key,
        "灯籠": tourou_key,
        "一目": ichi_key,
        "中目黒": nakame_key
    }

    for storename, api_key in api_key_dic.items():
        query = "accounts/current/checkouts"
        API_Endpoint = "https://ubiregi.com/api/3/{}".format(query)
        headers = {"X-Ubiregi-Auth-Token": api_key, "Content-Type": "application/json"}
        since_time = now.astimezone(JST)
        since_time = datetime.datetime.isoformat(since_time, timespec="seconds")
        since_time = since_time.replace(since_time[11:19], "04:00:00")
        # since_time = f"{day}T04:00:00+09:00"
        # since_time = f"2021-02-10T04:00:00+09:00"

        until_time = now.astimezone(JST)
        until_time = datetime.datetime.isoformat(until_time, timespec="seconds")
        # until_time = f"{str(day+datetime.timedelta(days=1))}T04:00:00+09:00"
        # until_time = f"2021-02-11T04:00:00+09:00"

        print(f"取得データ日時：{since_time} ~ {until_time}")
        params = {
            "since": f"{since_time}",
            "until": f"{until_time}",
            "total_count": "true",
        }
        res = requests.get(API_Endpoint, headers=headers, params=params).json()

        for s in res["checkouts"]:
            if s["status"] == "delete" or s["status"] == "cancel":
                paid_at = convert_str_to_datetime_jst(s["paid_at"])
                status = translate_status_to_japanese(s["status"])

                line_bot_list.append(f"【{storename}】")

                line_bot_list.append(paid_at[-8:])
                line_bot_list.append(status)


if __name__ == "__main__":
    notify_todays_illegal()
