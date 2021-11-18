from django.db import models


class PRED_data(models.Model):
    date = models.DateField("日付", null=False, blank=False, primary_key=True)
    week = models.CharField("曜日", max_length=2, null=False, blank=False)
    before_holiday = models.IntegerField("祝前日", null=False, blank=False)
    holiday = models.IntegerField("祝日", null=False, blank=False)
    weather_l = models.FloatField("天気:ランチ", null=True, blank=True)
    rain_l = models.FloatField("降水量:ランチ", null=True, blank=True)
    tempe_l = models.FloatField("気温:ランチ", null=True, blank=True)
    wind_l = models.FloatField("風速:ランチ", null=True, blank=True)
    weather_d = models.FloatField("天気:ディナー", null=True, blank=True)
    rain_d = models.FloatField("降水量:ディナー", null=True, blank=True)
    tempe_d = models.FloatField("気温:ディナー", null=True, blank=True)
    wind_d = models.FloatField("風速:ディナー", null=True, blank=True)
    # weather_tokyo_l = models.FloatField("天気東京:ランチ", null=True, blank=True)
    rain_tokyo_l = models.FloatField("降水量東京:ランチ", null=True, blank=True)
    tempe_tokyo_l = models.FloatField("気温東京:ランチ", null=True, blank=True)
    # wind_tokyo_l = models.FloatField("風速東京:ランチ", null=True, blank=True)
    # weather_tokyo_d = models.FloatField("天気東京:ディナー", null=True, blank=True)
    rain_tokyo_d = models.FloatField("降水量東京:ディナー", null=True, blank=True)
    tempe_tokyo_d = models.FloatField("気温東京:ディナー", null=True, blank=True)
    # wind_tokyo_d = models.FloatField("風速東京:ディナー", null=True, blank=True)
    corona_tokyo = models.FloatField("コロナ感染発表数:都内", null=True, blank=True)
    peopleflow_shibuya = models.FloatField("人流変化:渋谷", null=True, blank=True)
    state_of_emergency = models.IntegerField("緊急事態フラグ", null=True, blank=True)
    shorttime_at22 = models.IntegerField("時短22時", null=True, blank=True)
    shorttime_at20 = models.IntegerField("時短20時", null=True, blank=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "特徴量"
        verbose_name_plural = "特徴量"


class STORE_data(models.Model):
    store_name = models.CharField("店舗名", default="店舗名", max_length=15, null=False, blank=False)

    def __str__(self):
        return self.store_name

    class Meta:
        verbose_name = "店舗"
        verbose_name_plural = "店舗"


class CUSTOMER_data(models.Model):
    date = models.DateField("日付", null=False, blank=False)
    week = models.CharField("曜日", max_length=2, null=False, blank=False)
    store = models.ForeignKey(STORE_data, on_delete=models.PROTECT)
    cust_l = models.IntegerField("来客数:ランチ", null=True, blank=True)
    cust_d = models.IntegerField("来客数:ディナー", null=True, blank=True)
    price_l = models.IntegerField("売上:ランチ", null=True, blank=True)
    price_d = models.IntegerField("売上:ディナー", null=True, blank=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "売上データ"
        verbose_name_plural = "売上データ"
        constraints = [models.UniqueConstraint(fields=['date', 'store'], name="unique_datestore")]
