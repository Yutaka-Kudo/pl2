from django.db import models


class PL_data(models.Model):
    y_m = models.CharField("日付", null=False, default=199901, max_length=6)
    category = models.CharField("カテゴリー", null=False, default="カテゴリ", max_length=30)
    amountSold = models.IntegerField(verbose_name="総売上高", null=True, blank=True)
    rent = models.IntegerField("家賃", null=True, blank=True)

    def __str__(self):
        # return self.category + str(self.y_m)
        return self.category


class FoodCosts(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    cash_purchase_food = models.IntegerField("現金仕入れ(フード)", null=True, blank=True)
    ryque = models.IntegerField("リクエ", null=True, blank=True)
    ryqueFood = models.IntegerField("リクエ(フード)", null=True, blank=True)
    kitani_yumeya = models.IntegerField("キタニ水産/夢屋", null=True, blank=True)
    kitani = models.IntegerField("キタニ水産", null=True, blank=True)
    metroFood = models.IntegerField("メトロ(フード)", null=True, blank=True)
    metro = models.IntegerField("メトロ", null=True, blank=True)
    heiwameat = models.IntegerField("平和ミート", null=True, blank=True)
    heiwameat_kyoutan = models.IntegerField("平和ミート/京丹味噌（有）片山商店", null=True, blank=True)
    heiwameat_wanahakyoutan = models.IntegerField("平和ミート/罠は京丹味噌（有）片山商店", null=True, blank=True)
    heiwameat_wanahakyoutan2 = models.IntegerField("平和ミート/罠・京丹味噌（有）片山商店", null=True, blank=True)
    takanashiFood = models.IntegerField("タカナシ(フード)", null=True, blank=True)
    sunnyProducts = models.IntegerField("サニープロダクツ", null=True, blank=True)
    wakita_nouto = models.IntegerField("和喜多/5月分からノウト", null=True, blank=True)
    nouto = models.IntegerField("ノウト", null=True, blank=True)
    ryokyoryutsu_gogocurry = models.IntegerField("猟協流通/ゴーゴーカレー", null=True, blank=True)
    gogocurry = models.IntegerField("ゴーゴーカレー", null=True, blank=True)
    precoVegetables_yaotora = models.IntegerField("プレコフーズ(野菜)/八百虎・カネマン", null=True, blank=True)
    precoVegetables_kaneman_daiyu = models.IntegerField("プレコフーズ(野菜)/カネマン・ダイユウ", null=True, blank=True)
    preco_chacoal = models.IntegerField("プレコフーズ/廣備（炭）", null=True, blank=True)
    yaotora = models.IntegerField("八百虎", null=True, blank=True)
    begetarianButcher_nishihara = models.IntegerField("ベジタリアンブッチャー/西原商会", null=True, blank=True)
    nishihara = models.IntegerField("西原商会", null=True, blank=True)
    nishiharaFood = models.IntegerField("西原商会(フード)", null=True, blank=True)
    maruyasu_sunnyProducts_toho = models.IntegerField("マルヤス/サニープロダクツ(フード)/トーホーフード", null=True, blank=True)
    toho = models.IntegerField("トーホー", null=True, blank=True)
    tohoFood = models.IntegerField("トーホーフード", null=True, blank=True)
    precoMeat = models.IntegerField("プレコフーズ（肉）", null=True, blank=True)
    hirano_wanaYumeya = models.IntegerField("平野農園/罠　夢屋", null=True, blank=True)
    sanwaroland_wanaYumeya = models.IntegerField("サンワローラン/罠　夢屋", null=True, blank=True)
    marudai = models.IntegerField("丸大フード", null=True, blank=True)


class DrinkCosts(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    kakuyasuDrink = models.IntegerField("カクヤス(ドリンク)", null=True, blank=True)
    izumiyaDrink = models.IntegerField("いずみや（ドリンク）", null=True, blank=True)
    nestle = models.IntegerField("ネスレ", null=True, blank=True)
    yatsuya = models.IntegerField("やつや", null=True, blank=True)
    yatsuya_jenos = models.IntegerField("やつや/ジェノス", null=True, blank=True)
    yatsuya_jenos2 = models.IntegerField("やつや/中目罠ジェノス", null=True, blank=True)
    altcorporationWine = models.IntegerField("ｱﾙﾄｺｰﾎﾟﾚｰｼｮﾝ（ワイン）", null=True, blank=True)
    pieroth = models.IntegerField("ピーロートジャパン", null=True, blank=True)
    hashimoto = models.IntegerField("酒のはしもと", null=True, blank=True)
    drinkOther = models.IntegerField("その他(ドリンク)", null=True, blank=True)


class LaborCosts(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    labor_costs = models.IntegerField("人件費", null=True, blank=True)
    employee_costs = models.IntegerField("社員人件費", null=True, blank=True)
    partTimeWorker_costs = models.IntegerField("アルバイト人件費", null=True, blank=True)
    company_insurance_total = models.IntegerField("社保合計", null=True, blank=True)
    other_ex_dailyPayment = models.IntegerField("その他（日払い等）", null=True, blank=True)
    other_ex_dailyPayment2 = models.IntegerField("賞与社保合計/その他（日払い等）", null=True, blank=True)
    bonus = models.IntegerField("賞与", null=True, blank=True)
    transportationExpenses = models.IntegerField("交通費", null=True, blank=True)


class UtilityCosts_ComunicationCosts(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    gasFee = models.IntegerField("ガス代", null=True, blank=True)
    electricBill = models.IntegerField("電気代", null=True, blank=True)
    waterBill = models.IntegerField("上水道代", null=True, blank=True)
    sewerBill = models.IntegerField("下水道", null=True, blank=True)
    electricSavingCost = models.IntegerField("電気節電費", null=True, blank=True)
    electricSavingCost_lifest_arc = models.IntegerField("電気節電費（LIFFST・ｱｰｸｲﾝﾀｰﾅｼｮﾅﾙ）", null=True, blank=True)
    electricSavingCost_lifest = models.IntegerField("電気節電費（LIFFST）", null=True, blank=True)
    electricSavingCost_softbank = models.IntegerField("電気節電費/本部ソフトバンク携帯", null=True, blank=True)
    waterSavingCost = models.IntegerField("水道節水費", null=True, blank=True)
    waterSavingCost_wanaNakameguroLoan = models.IntegerField("水道節水費/罠中目黒　残存割賦金", null=True, blank=True)
    communicationCost = models.IntegerField("通信費", null=True, blank=True)
    ubiregi = models.IntegerField("ユビレジ", null=True, blank=True)
    usen = models.IntegerField("USEN", null=True, blank=True)
    internetFee = models.IntegerField("ネット代", null=True, blank=True)
    ubiregi_nhk = models.IntegerField("ユビレジ/NHK料金", null=True, blank=True)
    wanaNakameguroLoan = models.IntegerField("罠中目黒　残存割賦金", null=True, blank=True)
    willcom = models.IntegerField("ウィルコム", null=True, blank=True)
    willcom_yumeyaLicenseFee = models.IntegerField("ウィルコム/夢屋ライセンスフィー", null=True, blank=True)
    yumeyaLicenseFee = models.IntegerField("夢屋ライセンスフィー", null=True, blank=True)
    wanaNakameguroLoan_gasFee = models.IntegerField("罠中目黒　残存割賦金/中目借家ガス代", null=True, blank=True)


class AdvertisingCosts(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    advertisingGurunabi = models.IntegerField("広告費（ぐるなび）", null=True, blank=True)
    Gurunabi = models.IntegerField("ぐるなび", null=True, blank=True)
    advertisingHotpepper = models.IntegerField("広告費（ＨＰ）", null=True, blank=True)
    Hotpepper = models.IntegerField("ホットペッパー", null=True, blank=True)
    advertisingTabelog = models.IntegerField("食べログ(SGS)", null=True, blank=True)
    Tabelog = models.IntegerField("食べログ", null=True, blank=True)
    tLab = models.IntegerField("広告費（ぐるなび更新ティーラボ）", null=True, blank=True)
    hitosara_gururiza = models.IntegerField("ヒトサラ/ぐるりざ（10月～）", null=True, blank=True)
    roi_recoruHeadquarters = models.IntegerField("ROI（ファンくる・ぐるりざ）・本部レコル", null=True, blank=True)
    retty = models.IntegerField("レッティー", null=True, blank=True)
    fesMaipure_recoru = models.IntegerField("FESまいぷれ/本部レコル", null=True, blank=True)
    maipure = models.IntegerField("まいぷれ", null=True, blank=True)
    externalSalesCost_googleAds = models.IntegerField("外販委託料/グーグル広告", null=True, blank=True)
    externalSalesCost = models.IntegerField("外販委託料", null=True, blank=True)
    googleAds = models.IntegerField("グーグル広告", null=True, blank=True)
    jobAds = models.IntegerField("求人広告費", null=True, blank=True)
    chibadoyukai = models.IntegerField("千葉同友会費", null=True, blank=True)


class OtherCosts(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    askul = models.IntegerField("アクスル", null=True, blank=True)
    prenty = models.IntegerField("プレンティ", null=True, blank=True)
    expendables = models.IntegerField("消耗品(本部ビバホーム)", null=True, blank=True)
    regiLease = models.IntegerField("レジリース代", null=True, blank=True)
    expendables2 = models.IntegerField("消耗品", null=True, blank=True)
    other = models.IntegerField("その他", null=True, blank=True)
    expendables3 = models.IntegerField("消耗費", null=True, blank=True)
    garbageDisposal = models.IntegerField("ごみ処理費", null=True, blank=True)
    wetTowel_ootaki = models.IntegerField("お絞り代（大滝）", null=True, blank=True)
    pestControl = models.IntegerField("害虫駆除", null=True, blank=True)
    saniclean_drainagePipe = models.IntegerField("サニクリーン代/排水管清掃", null=True, blank=True)
    dyfil = models.IntegerField("ダイフィル", null=True, blank=True)
    altcorporation = models.IntegerField("アルトコーポレーション害虫駆除/エアコンフィルター", null=True, blank=True)
    toyoEnterprise = models.IntegerField("とよエンタープライス（設備リース）", null=True, blank=True)
    meetingCost = models.IntegerField("会議費", null=True, blank=True)
    inspectionCost = models.IntegerField("他店視察費", null=True, blank=True)
    entertainmentFee = models.IntegerField("接待交際費", null=True, blank=True)
    welfare = models.IntegerField("福利厚生費", null=True, blank=True)
    capitalInvestment = models.IntegerField("設備投資(備品、修理等、その他)", null=True, blank=True)
    housingAllowance = models.IntegerField("住宅手当", null=True, blank=True)
    companyHousingAllowance = models.IntegerField("社宅手当", null=True, blank=True)
    parkingLot = models.IntegerField("駐車場代", null=True, blank=True)
    vehicleCost = models.IntegerField("車両費", null=True, blank=True)
    labor_and_social_security_attorney = models.IntegerField("労務士報酬", null=True, blank=True)
    tax_accountant = models.IntegerField("税理士報酬", null=True, blank=True)
    update2 = models.IntegerField("家賃　更新代", null=True, blank=True)
    update = models.IntegerField("家賃　更新代 補償金", null=True, blank=True)
    subsidy = models.IntegerField("補助金", null=True, blank=True)


class TaxExemptExpenses(models.Model):
    pl_data = models.ForeignKey(PL_data, on_delete=models.CASCADE)
    insuranceFee = models.IntegerField("保険料（店舗・自動車・労災・車検）", null=True, blank=True)
    insuranceFee2 = models.IntegerField("保険料（店舗・自動車・労災）", null=True, blank=True)
    repayment = models.IntegerField("返済", null=True, blank=True)
    insuranceFee_fesRepayment = models.IntegerField("保険料/FES返済（店舗・自動車・労災）", null=True, blank=True)
    repayment1 = models.IntegerField("①返済", null=True, blank=True)
    repayment2 = models.IntegerField("②返済", null=True, blank=True)
    repayment3 = models.IntegerField("③返済", null=True, blank=True)
    repayment4 = models.IntegerField("④返済", null=True, blank=True)
    prudential1 = models.IntegerField("①プルデンシャル", null=True, blank=True)
    prudential2 = models.IntegerField("②プルデンシャル", null=True, blank=True)
    creditCard_rakutensmp1 = models.IntegerField("①クレジットカード手数料【楽天スマぺ】", null=True, blank=True)
    creditCard_chibabank2 = models.IntegerField("②クレジットカード手数料【千葉銀行】", null=True, blank=True)
    taxEffect = models.IntegerField("租税効果(法人税・住民税等)", null=True, blank=True)
    insuranceFee_store_industrialAccident = models.IntegerField("保険料（店舗・労災）", null=True, blank=True)
    insuranceFee_car_inspection = models.IntegerField("保険料（自動車・車検）", null=True, blank=True)
    bankruptcy_prevention = models.IntegerField("倒産防止共済", null=True, blank=True)
    creditCard_rakuten2 = models.IntegerField("クレジットカード手数料【楽天スマぺ】", null=True, blank=True)
    creditCard_rakuten = models.IntegerField("クレジットカード手数料【楽天スマぺ】本部プルデンシャル生命", null=True, blank=True)
    creditCard_zentoshin = models.IntegerField("クレジットカード手数料【全東信】本部プルデンシャル", null=True, blank=True)
    creditCard_zentoshin2 = models.IntegerField("クレジットカード手数料【全東信】", null=True, blank=True)

