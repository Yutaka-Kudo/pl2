# Generated by Django 3.2.8 on 2021-11-26 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_part', '0006_rename_labor9_laborcosts_transportationexpenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisingcosts',
            name='ad13',
            field=models.IntegerField(blank=True, null=True, verbose_name='UBER'),
        ),
        migrations.AlterField(
            model_name='advertisingcosts',
            name='ad6',
            field=models.IntegerField(blank=True, null=True, verbose_name='食べログ'),
        ),
        migrations.AlterField(
            model_name='advertisingcosts',
            name='ad8',
            field=models.IntegerField(blank=True, null=True, verbose_name='広告費'),
        ),
        migrations.AlterField(
            model_name='utilitycosts_comunicationcosts',
            name='util18',
            field=models.IntegerField(blank=True, null=True, verbose_name='フィルコム'),
        ),
        migrations.AlterField(
            model_name='utilitycosts_comunicationcosts',
            name='util19',
            field=models.IntegerField(blank=True, null=True, verbose_name='フィルコム'),
        ),
    ]
