from django.db import models


class Progress(models.Model):
    """進捗管理モデル"""

    now = models.IntegerField("現在の進捗", default=0)
    total = models.IntegerField("全ステップ数", default=100)


class TargetFileName(models.Model):
    """ファイルが開かれているため重複ファイルを作った際の、それ以降のファイル名の管理"""
    store = models.CharField(null=False, default="店名", max_length=30)
    file_name = models.CharField(null=False, default="店名", max_length=100)


class Costs(models.Model):
    store = models.CharField(null=False, default="店名", max_length=30)
    salary = models.IntegerField('社員給料', default=0)
    hourly_wage = models.IntegerField('バイト時給', default=0)
    rent = models.IntegerField('家賃', default=0)
    rent_renewal = models.IntegerField('家賃更新代', default=0)
    renewal_frequency = models.IntegerField('家賃更新頻度/年', default=0)
    yumeya_fee = models.IntegerField('夢屋ライセンスフィー', default=0)
    utility_cost = models.IntegerField('光熱費', default=0)
    ad_cost = models.IntegerField('広告費', default=0)
    other_total = models.IntegerField('その他諸経費', default=0)
