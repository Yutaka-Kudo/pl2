from django.http.response import HttpResponse
from django.shortcuts import render
import requests
import datetime
from pprint import pprint as pp
import os
from dotenv import load_dotenv

from display_part.views import category_list


def delete_and_cancel_checker(request):
    day_for_html = request.GET.get("q")
    day = request.GET.get("q").replace("/", "-")
    day = datetime.date.fromisoformat(day)

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

    load_dotenv()
    api_key_dic = {
        "FES": os.environ["UBIREGI_FES_KEY"],
        "Garage": os.environ["UBIREGI_GARAGE_KEY"],
        "灯籠": os.environ["UBIREGI_TOUROU_KEY"],
        "一目": os.environ["UBIREGI_ICHI_KEY"],
        "中目黒": os.environ["UBIREGI_NAKAME_KEY"],
    }

    result_list = []
    total_count = 0

    for storename, api_key in api_key_dic.items():
        query = "accounts/current/checkouts"
        API_Endpoint = "https://ubiregi.com/api/3/{}".format(query)
        headers = {"X-Ubiregi-Auth-Token": api_key, "Content-Type": "application/json"}
        JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
        # today = datetime.datetime.now() - datetime.timedelta(hours=9)-datetime.timedelta(days=1)
        # today = datetime.datetime.isoformat(today, timespec="seconds")[:11]+"19:00:00"
        today = f"{day}T04:00:00+09:00"

        # now = datetime.datetime.now() - datetime.timedelta(hours=9)
        # now = datetime.datetime.isoformat(now, timespec="seconds")
        now = f"{str(day+datetime.timedelta(days=1))}T04:00:00+09:00"
        params = {
            "since": f"{today}",
            "until": f"{now}",
            "total_count": "true",
        }
        res = requests.get(API_Endpoint, headers=headers, params=params).json()

        result_list.append("■■■■■■■■■■■■■■■■")

        result_list.append(f"【{storename}】")

        case_count = 0

        for s in res["checkouts"]:
            judge_count = 0
            if s["status"] == "delete" or s["status"] == "cancel":
                total_count += 1
                case_count += 1
                if case_count != 1:
                    result_list.append("-----------------------")
                result_list.append("〜ケース " + str(case_count) + "〜")

                # データ前処理
                paid_at = convert_str_to_datetime_jst(s["paid_at"])
                status = translate_status_to_japanese(s["status"])
                if not s["memo"]:
                    s["memo"] = ""

                result_list.append("処理ID:" + str(s["id"]))
                result_list.append(paid_at)
                result_list.append(status)
                result_list.append(s["memo"] + "卓")
                result_list.append(r"¥" + "{:,}".format(int(s["price"][:-2])))

                for ss in res["checkouts"]:
                    if convert_str_to_datetime_jst(s["paid_at"]) != convert_str_to_datetime_jst(ss["paid_at"]):
                        if ss["memo"] == s["memo"] or ss["table_ids"] == s["table_ids"] or ss["price"] == s["price"] or ss["id"] == s["id"]:
                            if judge_count == 0:
                                result_list.append("〜判断材料〜")
                                judge_count += 1

                            # データ前処理
                            paid_at = convert_str_to_datetime_jst(ss["paid_at"])
                            status = translate_status_to_japanese(ss["status"])
                            if not ss["memo"]:
                                ss["memo"] = ""

                            result_list.append("処理ID:" + str(ss["id"]))
                            result_list.append(paid_at)
                            if datetime.datetime.fromisoformat(s["paid_at"].replace('Z', ''))-datetime.timedelta(hours=1) < datetime.datetime.fromisoformat(ss["paid_at"].replace('Z', '')) < datetime.datetime.fromisoformat(s["paid_at"].replace('Z', ''))+datetime.timedelta(hours=1):
                                result_list[-1] += "*"
                            result_list.append(status)
                            result_list.append(ss["memo"] + "卓")
                            if ss["memo"] == s["memo"]:
                                result_list[-1] += "*"
                            result_list.append(r"¥" + "{:,}".format(int(ss["price"][:-2])))
                            if ss["price"] == s["price"]:
                                result_list[-1] += "*"

    result_list.append("■■■■■■■■■■■■■■■■")

    # pp(result_list)

    context = {
        "total_count": total_count,
        "result_list": result_list,
        "cgy_list": category_list,
        "day_for_html": day_for_html,
    }
    return render(request, "display_part/index.html", context)
