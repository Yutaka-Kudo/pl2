from datetime import date
import datetime
from pandas.core.frame import DataFrame
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd

from prediction.models import PRED_data, CUSTOMER_data, STORE_data
from site_package.my_module import create_fieldname_dict, drop_list


def create_dfcust(store_name: str, to_day: date, previous_date: str = ""):
    store = STORE_data.objects.get(store_name=store_name)
    if previous_date:
        obj = CUSTOMER_data.objects.filter(store=store, date__icontains=previous_date).order_by('-date').values("date", "cust_l", "cust_d")
    else:
        obj = CUSTOMER_data.objects.filter(date__lt=to_day, store=store).values("date", "cust_l", "cust_d")
    df_cust = pd.DataFrame(list(obj))
    dbdict = create_fieldname_dict(CUSTOMER_data)
    df_cust.rename(columns=dbdict, inplace=True)
    df_cust = df_cust.set_index('日付').sort_index()

    return df_cust


def create_dfpredict(start_date: str = "", end_date: str = "", for_peopleflow: bool = False, previous_date: str = ""):
    if for_peopleflow is True:
        obj = PRED_data.objects.all()
    elif start_date:
        obj = PRED_data.objects.filter(date__gte=start_date, date__lte=end_date)
    elif previous_date:
        obj = PRED_data.objects.filter(date__icontains=previous_date)
    else:
        obj = PRED_data.objects.all().order_by('-date')[36:81]
    df_predict = pd.DataFrame(list(obj.values()))
    dbdict = create_fieldname_dict(PRED_data)
    df_predict.rename(columns=dbdict, inplace=True)
    df_predict = df_predict.set_index('日付').sort_index()
    df_predict = pd.concat([df_predict, pd.get_dummies(df_predict["曜日"])], axis=1)
    # print('df_predict')
    # print(df_predict)
    return df_predict


def create_dftrain(to_day: date, nakame_flg: bool = False):
    if nakame_flg is True:
        obj = PRED_data.objects.filter(date__lt=to_day, date__gte=date(2020, 10, 11)).values()
    else:
        obj = PRED_data.objects.filter(date__lt=to_day).values()
    df_train = pd.DataFrame(list(obj))
    dbdict = create_fieldname_dict(PRED_data)
    df_train.rename(columns=dbdict, inplace=True)
    df_train = df_train.set_index('日付').sort_index()
    df_train = pd.concat([df_train, pd.get_dummies(df_train["曜日"])], axis=1)

    return df_train


def drop_make_df(df: DataFrame, store: str):
    # 店ごとに微調整
    if store == "fes":
        df_x_l = df.drop(columns=drop_list["fes_l"])
        df_x_d = df.drop(columns=drop_list["fes_d"])
    elif store == "garage":
        df_x_l = df.drop(columns=drop_list["garage_l"])
        df_x_d = df.drop(columns=drop_list["garage_d"])
    elif store == "tourou":
        df_x_l = df.drop(columns=drop_list["tourou_l"])
        df_x_d = df.drop(columns=drop_list["tourou_d"])
    elif store == "wanaichi":
        df_x_l = df.drop(columns=drop_list["wanaichi_l"])
        df_x_d = df.drop(columns=drop_list["wanaichi_d"])
    elif store == "wananakame":
        df_x_l = df.drop(columns=drop_list["wananakame_l"])
        df_x_d = df.drop(columns=drop_list["wananakame_d"])
    elif store == "corona_tokyo":
        df_x_l = df.drop(columns=drop_list["corona_tokyo"])
        df_x_d = None
    elif store == "people":
        df_x_l = df.drop(columns=drop_list["people"])
        df_x_d = None
    else:
        df_x_l, df_x_d = None, None
        raise Exception('drop_make_df store名がおかしいです。')

    return df_x_l, df_x_d


def customer_learning(store: str, to_day: date):
    if store == "wananakame":
        df_train = create_dftrain(to_day, nakame_flg=True)
    else:
        df_train = create_dftrain(to_day)
    df_cust = create_dfcust(store, to_day)
    df_train = pd.concat([df_train, df_cust], axis=1, sort=True)

    # ["来客数:ディナー"]にnullがあれば例外処理
    if df_train.isnull().sum()["来客数:ディナー"] > 0:
        null_judge_df = df_train.isnull()["来客数:ディナー"]
        null_judge_df = null_judge_df[null_judge_df == True]
        raise Exception(f'df_custデータに欠損があります。{list(null_judge_df.index)}')

    # df_cust = create_dfcust(store, to_day)[0:-16]  # これで一部除いて学習できる。
    # df_train = pd.concat([df_train, df_cust], axis=1, sort=True)[0:-16]
    # print(df_cust)
    # print(df_train)

    for index, i in df_train.iterrows():  # 店休日おとし
        if int(i["来客数:ランチ"]) == 0 and int(i["来客数:ディナー"]) == 0:
            if index <= datetime.date(2021, 3, 7) or index > to_day:
                df_train.drop(index, inplace=True)

    df_x_l, df_x_d = drop_make_df(df_train, store)
    # print(df_x_d)

    df_t_l = df_train['来客数:ランチ']
    df_t_d = df_train['来客数:ディナー']

    x_train_l, x_test_l, t_train_l, t_test_l = train_test_split(df_x_l, df_t_l, test_size=0.3, random_state=1)
    x_train_d, x_test_d, t_train_d, t_test_d = train_test_split(df_x_d, df_t_d, test_size=0.3, random_state=1)

    if store == "fes":
        model_l = GradientBoostingRegressor(random_state=0, learning_rate=0.06, max_depth=3,
                                            max_features=6, min_samples_split=2, n_estimators=100, subsample=1)
        model_d = RandomForestRegressor(random_state=1, max_depth=8, max_features=9, min_samples_split=12, n_estimators=100)
    elif store == "garage":
        model_l = RandomForestRegressor(random_state=0, max_depth=5, max_features=7, min_samples_split=5, n_estimators=10)
        model_d = RandomForestRegressor(random_state=1, max_depth=8, max_features=9, min_samples_split=12, n_estimators=100)
    elif store == "tourou":
        model_l = RandomForestRegressor(random_state=0, max_depth=5, max_features=7, min_samples_split=5, n_estimators=10)
        model_d = RandomForestRegressor(random_state=1, max_depth=8, max_features=9, min_samples_split=12, n_estimators=100)
    elif store == "wanaichi":
        model_l = RandomForestRegressor(random_state=0, max_depth=5, max_features=7, min_samples_split=5, n_estimators=10)
        model_d = RandomForestRegressor(random_state=0, max_depth=5, max_features=4, min_samples_split=12, n_estimators=60)
    elif store == "wananakame":
        model_l = RandomForestRegressor(random_state=0, max_depth=5, max_features=7, min_samples_split=5, n_estimators=10)
        model_d = LinearRegression()
        # model_d = RandomForestRegressor(random_state=0, max_depth=5, max_features=4, min_samples_split=12, n_estimators=100)

    model_l.fit(x_train_l, t_train_l)
    score_train_l = model_l.score(x_train_l, t_train_l)
    score_test_l = model_l.score(x_test_l, t_test_l)
    print(f"ランチtrainスコア  ： {score_train_l}")
    print(f"ランチtestスコア   ： {score_test_l}")
    accuracy_rate_l = (score_train_l + score_test_l) / 2
    accuracy_rate_l = str(round(accuracy_rate_l * 100, 2)) + "%"

    model_d.fit(x_train_d, t_train_d)
    score_train_d = model_d.score(x_train_d, t_train_d)
    score_test_d = model_d.score(x_test_d, t_test_d)
    print(f"ディナーtrainスコア： {score_train_d}")
    print(f"ディナーtestスコア ： {score_test_d}")
    accuracy_rate_d = (score_train_d + score_test_d) / 2
    accuracy_rate_d = str(round(accuracy_rate_d * 100, 2)) + "%"

    return model_l, model_d, accuracy_rate_l, accuracy_rate_d


def people_flow_learning(to_day: date):
    df_train = create_dftrain(to_day)
    df_x, _ = drop_make_df(df_train, "people")

    df_t = df_train['人流変化:渋谷']

    x_train, x_test, t_train, t_test = train_test_split(df_x, df_t, test_size=0.3, random_state=0)

    model = RandomForestRegressor(random_state=0, max_depth=5, max_features=7, min_samples_split=5, n_estimators=10)

    model.fit(x_train, t_train)
    score_train = model.score(x_train, t_train)
    score_test = model.score(x_test, t_test)
    print(f"人流trainスコア  ： {score_train}")
    print(f"人流testスコア   ： {score_test}")

    # 様子出力用ーーーーーーー
    # df_predict = create_dfpredict()
    # df_predict, _ = drop_make_df(df_predict, "people")
    # pred = model.predict(df_predict)
    # print(pred)

    return model


def corona_tokyo_learning(to_day: date):
    df_train = create_dftrain(to_day)
    df_x, _ = drop_make_df(df_train, "corona_tokyo")

    df_t = df_train['コロナ感染発表数:都内']

    # df_train.to_csv('~/desktop/corona_train.csv')

    x_train, x_test, t_train, t_test = train_test_split(df_x, df_t, test_size=0.3, random_state=0)

    model = GradientBoostingRegressor(random_state=0, learning_rate=0.07, max_depth=2, max_features=3, min_samples_split=3, n_estimators=100, subsample=0.6)

    model.fit(x_train, t_train)
    score_train = model.score(x_train, t_train)
    score_test = model.score(x_test, t_test)
    print(f"感染者trainスコア  ： {score_train}")
    print(f"感染者testスコア   ： {score_test}")

    # 様子出力用ーーーーーーー
    # df_predict = create_dfpredict()
    # df_predict, _ = drop_make_df(df_predict, "people")
    # pred = model.predict(df_predict)
    # print(pred)

    return model
