from django.test import TestCase
from unittest import mock
from django.shortcuts import resolve_url

import datetime as dt
import os

from . import views, models
from .actions import graph_helper

from dotenv import load_dotenv
load_dotenv()

# Create your tests here.







class Daily_reportTest(TestCase):
    def test_get_time(self):
        os.environ['TZ'] = 'Asia/Tokyo'
        to_day, now = views.get_time()
        os.environ['TZ'] = 'us'
        to_day2, now2 = views.get_time()

        now = now.isoformat(timespec='minutes')
        now2 = now2 + dt.timedelta(hours=9)  # 9時間差
        now2 = now2.isoformat(timespec='minutes')
        self.assertEqual(now, now2)

    def mock_initialize_context(self):
        return {'user': {'email': os.environ['MS_ID']}}

    @mock.patch('daily_report.views.initialize_context', mock_initialize_context)
    def test_home(self):
        res = self.client.get(resolve_url('daily_report:home'))
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.context.get('store_name'))

    def test_select_filename(self):
        name_for_file = 'FES'
        store_name = 'fes'
        to_day = dt.datetime(2021, 10, 9).date()
        test_name = 'テスト用'

        # DBに入ってなければ
        target_file_name = graph_helper.select_filename(name_for_file, store_name, to_day, test_name, models)
        self.assertEqual(target_file_name, f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}.xlsx')

        # 複製があれば
        models.TargetFileName.objects.filter(store='fes').update(file_name=f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}_複製1.xlsx')
        target_file_name = graph_helper.select_filename(name_for_file, store_name, to_day, test_name, models)
        self.assertEqual(target_file_name, f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}_複製1.xlsx')

        # 複製があれば2
        models.TargetFileName.objects.filter(store='fes').update(file_name=f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}_複製2.xlsx')
        target_file_name = graph_helper.select_filename(name_for_file, store_name, to_day, test_name, models)
        self.assertEqual(target_file_name, f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}_複製2.xlsx')

        # 月が進んだら
        to_day = dt.datetime(2021, 11, 9).date()
        target_file_name = graph_helper.select_filename(name_for_file, store_name, to_day, test_name, models)
        self.assertEqual(target_file_name, f'【{name_for_file}】{to_day.year}{str(to_day.month).zfill(2)}{test_name}.xlsx')
