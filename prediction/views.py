from prediction import ml, models
from display_part.views import pred_date_list, pred_date_list_reversed, previous_date_list
from site_package.my_module import trans_date

from django.shortcuts import render
from devtools import debug

import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

to_day = datetime.datetime.now().date() - relativedelta(days=1)


def show_chart(request, store_str):
    if request.GET.get('store'):
        req = request.GET.get('store')
        store_str = "fes" if req == "FES" else "garage" if req == "Garage" else "tourou" if req == "灯篭" else "wanaichi" if req == "罠一目" else "wananakame" if req == "罠中目黒" else None
    previous_date = request.GET.get('previous_date')
    move = request.GET.get('move')
    if move == "before":
        p = datetime.datetime.strptime(previous_date, "%Y-%m")-relativedelta(months=1)
        previous_date = datetime.date.strftime(p, '%Y-%m')
    elif move == "after":
        p = datetime.datetime.strptime(previous_date, "%Y-%m")+relativedelta(months=1)
        previous_date = datetime.date.strftime(p, '%Y-%m')
    model_l, model_d, accuracy_rate_l, accuracy_rate_d = ml.customer_learning(store_str, to_day)
    context = create_data(store_str, model_l, model_d, previous_date=previous_date)
    context["accuracy_l"] = accuracy_rate_l
    context["accuracy_d"] = accuracy_rate_d
    context["previous_date_list"] = previous_date_list
    return render(request, "prediction/chart.html", context)


def show_chart_long(request, store_str):
    if request.GET.get('store'):
        req = request.GET.get('store')
        store_str = "fes" if req == "FES" else "garage" if req == "Garage" else "tourou" if req == "灯篭" else "wanaichi" if req == "罠一目" else "wananakame" if req == "罠中目黒" else None
    if request.GET.get('this_month'):  # 今月
        this_month_first = datetime.datetime.now() + relativedelta(day=1)
        start_date: str = this_month_first.strftime('%Y-%m-%d')
        end_date: str = (this_month_first + relativedelta(months=1) - relativedelta(days=1)).strftime('%Y-%m-%d')
    if request.GET.get('pred_start_date'):
        start_date = request.GET.get('pred_start_date')
        end_date = request.GET.get('pred_end_date')
    model_l, model_d, accuracy_rate_l, accuracy_rate_d = ml.customer_learning(store_str, to_day)
    context = create_data(store_str, model_l, model_d, start_date=start_date, end_date=end_date)
    context["accuracy_l"] = accuracy_rate_l
    context["accuracy_d"] = accuracy_rate_d
    context["pred_date_list"] = pred_date_list
    context["pred_date_list_reversed"] = pred_date_list_reversed
    context["this_month"] = request.GET.get('this_month')
    return render(request, "prediction/chart_long.html", context)


def create_data(store_str: str, model_l, model_d, start_date: str = "", end_date: str = "", previous_date=""):

    store_obj = models.STORE_data.objects.get(store_name=store_str)

    # 単価取得 2ヶ月前までのーーーーーーーーーーー
    two_month_ago = to_day - relativedelta(months=2)
    qs = models.CUSTOMER_data.objects.filter(store=store_obj, date__gte=two_month_ago)
    total_cust_l, total_cust_d, total_price_l, total_price_d = 0, 0, 0, 0
    for q in qs:
        total_cust_l += q.cust_l
        total_cust_d += q.cust_d
        total_price_l += q.price_l
        total_price_d += q.price_d
    unit_price_l: float = total_price_l / total_cust_l
    unit_price_d: float = total_price_d / total_cust_d
    # ーーーーーーーーーーーーーーーーーーーーーー単価取得終了

    if previous_date:
        df_predict = ml.create_dfpredict(previous_date=previous_date)
        df_cust = ml.create_dfcust(store_str, to_day, previous_date=previous_date)
        df_predict = pd.concat([df_predict, df_cust], axis=1, sort=True)
        df_predict.fillna({"来客数:ランチ": 0, "来客数:ディナー": 0}, inplace=True)

        store = models.STORE_data.objects.get(store_name=store_str)
        obj = models.CUSTOMER_data.objects.filter(store=store).latest('date')
        debug(obj.date)

        for index, i in df_predict.iterrows():  # 店休日と未来はカット
            if int(i["来客数:ランチ"]) == 0 and int(i["来客数:ディナー"]) == 0:
                if index <= datetime.date(2021, 3, 7) or index > obj.date:
                    df_predict.drop(index, inplace=True)

    else:
        df_predict = ml.create_dfpredict(start_date, end_date)
        df_predict["来客数:ランチ"] = 1  # つけないとml.drop_make_dfでエラーる
        df_predict["来客数:ディナー"] = 1  # つけないとml.drop_make_dfでエラーる

    lunch_x, dinner_x = ml.drop_make_df(df_predict, store_str)
    # print(lunch_x)

    pred_l = np.round(model_l.predict(lunch_x))

    index = [datetime.date.strftime(s, '%Y-%m-%d')[5:] for s in df_predict.index]
    xticks = list(index + df_predict["曜日"])

    dayList = [x[-3:] for x in xticks]

    pred_d = np.round(model_d.predict(dinner_x))

    if previous_date:
        # 実際売上関連ーーーーーーーーーーーーーーーー
        this_month_first = to_day - relativedelta(day=1)
        qs = models.CUSTOMER_data.objects.filter(store=store_obj, date__gte=this_month_first)

        actually_daily_sales_l = []
        actually_daily_sales_d = []
        actually_amount_sales_l, actually_amount_sales_d = 0, 0
        actually_amount_sales_l_forTable = []
        actually_amount_sales_d_forTable = []

        for q in qs:
            actually_daily_sales_l.append(round(q.price_l / 10000, 1))
            actually_daily_sales_d.append(round(q.price_d / 10000, 1))
            actually_amount_sales_l += q.price_l
            actually_amount_sales_d += q.price_d
            actually_amount_sales_l_forTable.append(round(actually_amount_sales_l / 10000, 1))
            actually_amount_sales_d_forTable.append(round(actually_amount_sales_d / 10000, 1))
        # ーーーーーーーーーーーーーーーー実際売上関連終了

        # 予測売上関連ーーーーーーーーーーーーーーーーーーーーー
        # ランチ売上リスト
        sales_list_l = pred_l * unit_price_l
        # 万単位で表示するため丸める
        pred_daily_sales_l = [round((i/10000), 1) for i in sales_list_l]
        total_sales_pred_l = sum(sales_list_l)

        # ディナー売上リスト
        sales_list_d = pred_d * unit_price_d
        # 万単位で表示するため丸める
        pred_daily_sales_d = [round((i/10000), 1) for i in sales_list_d]
        total_sales_pred_d = sum(sales_list_d)

        # 日ごと売上
        daily_total_sales_forTable = [round(a+b, 1) for a, b in zip(pred_daily_sales_l, pred_daily_sales_d)]

        # 累計売上表 ランチ
        pred_amount_sales = 0
        pred_amount_sales_forTable_l = []
        for sales in pred_daily_sales_l:
            pred_amount_sales += sales
            pred_amount_sales_forTable_l.append(round(pred_amount_sales, 1))
        # 累計売上表 ディナー
        pred_amount_sales = 0
        pred_amount_sales_forTable_d = []
        for sales in pred_daily_sales_d:
            pred_amount_sales += sales
            pred_amount_sales_forTable_d.append(round(pred_amount_sales, 1))
        # 累計売上表
        pred_amount_sales = 0
        pred_amount_sales_forTable = []
        for sales in daily_total_sales_forTable:
            pred_amount_sales += sales
            pred_amount_sales_forTable.append(round(pred_amount_sales, 1))
        # ーーーーーーーーーーーーーーーーーーーーー予測売上関連終了

        # df_forTable_l = pd.DataFrame([pred_l, df_predict["来客数:ランチ"].values], index=["予測", "実際"], columns=df_predict.index).astype('int')
        df_forTable_l = pd.DataFrame([pred_l, df_predict["来客数:ランチ"].values], index=["予測", "実際"], columns=df_predict.index).astype('int')
        df_forTable_d = pd.DataFrame([pred_d, df_predict["来客数:ディナー"].values], index=["予測", "実際"], columns=df_predict.index).astype('int')
        actually_l = list(df_predict["来客数:ランチ"])
        actu_total_l = round(sum(actually_l))
        pred_list_l = list(pred_l)
        pred_total_l = round(sum(pred_list_l))
        actually_d = list(df_predict["来客数:ディナー"])
        actu_total_d = round(sum(actually_d))
        pred_list_d = list(pred_d)
        pred_total_d = round(sum(pred_list_d))

        context = {
            "actually_l": actually_l,
            "actually_d": actually_d,
            "actu_total_l": actu_total_l,
            "actu_total_d": actu_total_d,
            "actually_daily_sales_l": actually_daily_sales_l,
            "actually_daily_sales_d": actually_daily_sales_d,
            "actually_amount_sales_l_forTable": actually_amount_sales_l_forTable,
            "actually_amount_sales_d_forTable": actually_amount_sales_d_forTable,

            "pred_l": pred_list_l,
            "pred_d": pred_list_d,
            "pred_total_l": pred_total_l,
            "pred_total_d": pred_total_d,
            "pred_daily_sales_l": pred_daily_sales_l,
            "pred_daily_sales_d": pred_daily_sales_d,
            "pred_amount_sales_forTable_l": pred_amount_sales_forTable_l,
            "pred_amount_sales_forTable_d": pred_amount_sales_forTable_d,

            "daily_total_sales_forTable": daily_total_sales_forTable,

            "unit_price_l": round(unit_price_l),
            "unit_price_d": round(unit_price_d),

            "xticks": xticks,
            "df_forTable_l": df_forTable_l,
            "df_forTable_d": df_forTable_d,
            "dayList": dayList,
            "store_str": store_str,
            "previous_date": previous_date,
        }

    else:
        # sales_l_list = ["{:,.0f}".format(i) for i in pred_l * unit_price_l]
        # ランチ売上リスト
        sales_list_l = pred_l * unit_price_l
        # 万単位で表示するため丸める
        saleslist_forTable_l = [round((i/10000), 1) for i in sales_list_l]
        total_sales_pred_l = sum(sales_list_l)

        # ディナー売上リスト
        sales_list_d = pred_d * unit_price_d
        # 万単位で表示するため丸める
        saleslist_forTable_d = [round((i/10000), 1) for i in sales_list_d]
        total_sales_pred_d = sum(sales_list_d)

        # 日ごと累計売上
        daily_total_sales_forTable = [round(a+b, 1) for a, b in zip(saleslist_forTable_l, saleslist_forTable_d)]
        # 累計売上表
        amount_sales = 0
        amount_sales_forTable = []
        for i, sales in enumerate(daily_total_sales_forTable):
            amount_sales += sales
            amount_sales_forTable.append(round(amount_sales, 1))

        df_forTable_l = pd.DataFrame([pred_l], index=["客数"], columns=df_predict.index).astype('int')
        df_forTable_d = pd.DataFrame([pred_d], index=["客数"], columns=df_predict.index).astype('int')

        pred_list_l = list(pred_l)
        pred_total_l = round(sum(pred_list_l))
        pred_list_d = list(pred_d)
        pred_total_d = round(sum(pred_list_d))

        required_people_l = []
        for i in sales_list_l:  # 必要人員ーーーーーー
            if i < 50000:
                required_people_l.append(2)
            elif i < 100000:
                required_people_l.append(3)
            elif i < 150000:
                required_people_l.append(4)
            elif i < 200000:
                required_people_l.append(5)
            elif i < 250000:
                required_people_l.append(6)
            elif i < 300000:
                required_people_l.append(7)
            elif i < 350000:
                required_people_l.append(8)
            else:
                required_people_l.append(9)

        required_people_d = []
        for i in sales_list_d:
            if i < 50000:
                required_people_d.append(2)
            elif i < 100000:
                required_people_d.append(3)
            elif i < 150000:
                required_people_d.append(4)
            elif i < 200000:
                required_people_d.append(5)
            elif i < 250000:
                required_people_d.append(6)
            elif i < 300000:
                required_people_d.append(7)
            elif i < 350000:
                required_people_d.append(8)
            else:
                required_people_d.append(9)

        context = {
            "pred_l": pred_list_l,
            "pred_d": pred_list_d,
            "pred_total_l": pred_total_l,
            "pred_total_d": pred_total_d,
            "xticks": xticks,
            "df_forTable_l": df_forTable_l,
            "df_forTable_d": df_forTable_d,
            "saleslist_forTable_l": saleslist_forTable_l,
            "saleslist_forTable_d": saleslist_forTable_d,
            "daily_total_sales_forTable": daily_total_sales_forTable,
            "amount_sales_forTable": amount_sales_forTable,
            "required_people_l": required_people_l,
            "required_people_d": required_people_d,
            "total_sales_pred_l": "{:,.0f}".format(total_sales_pred_l),
            "total_sales_pred_d": "{:,.0f}".format(total_sales_pred_d),
            "total_pred_price": "{:,.0f}".format(total_sales_pred_l+total_sales_pred_d),
            "unit_price_l": round(unit_price_l),
            "unit_price_d": round(unit_price_d),
            "dayList": dayList,
            "store_str": store_str,
            "start_date": start_date,
            "end_date": end_date,
        }

    return context
