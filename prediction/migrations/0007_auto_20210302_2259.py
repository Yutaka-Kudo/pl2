# Generated by Django 3.1.7 on 2021-03-02 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0006_auto_20210302_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pred_data',
            name='weather_tokyo_d',
        ),
        migrations.RemoveField(
            model_name='pred_data',
            name='weather_tokyo_l',
        ),
        migrations.RemoveField(
            model_name='pred_data',
            name='wind_tokyo_d',
        ),
        migrations.RemoveField(
            model_name='pred_data',
            name='wind_tokyo_l',
        ),
    ]
