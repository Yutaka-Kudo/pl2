# Generated by Django 3.2.3 on 2021-08-14 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_part', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisingcosts',
            name='chibadoyukai',
            field=models.IntegerField(blank=True, null=True, verbose_name='千葉同友会費'),
        ),
    ]
