from django.db import models

# Create your models here.


class Managers(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    c_d_permission = models.BooleanField('登録削除権限', default=False)
