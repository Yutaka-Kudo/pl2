from django.test import TestCase
from unittest import mock
from django.shortcuts import resolve_url
from django.urls import reverse

import datetime as dt
import os

from icecream import ic
import dictdiffer

from . import views, models
from .actions import graph_helper

from dotenv import load_dotenv
load_dotenv()


class HomeTest(TestCase):
    def test_home_output(self):

        # compare screen displays
        res = self.client.get(reverse('daily_report:home'))
        res_as_view = self.client.get(reverse('daily_report:home2'))
        self.assertEqual(res.content, res_as_view.content)

        # compare contexts
        con1 = dict(res.context)
        con2 = dict(res_as_view.context)
        exclude_keylist = ['csrf_token', 'messages', 'perms', 'view', 'request']
        con1 = {k: v for k, v in con1.items() if k not in exclude_keylist}
        con2 = {k: v for k, v in con2.items() if k not in exclude_keylist}
        if con1['now'] - dt.timedelta(seconds=10) <= con2['now'] <= con1['now'] + dt.timedelta(seconds=10):  # ±10秒を許容
            con2['now'] = con1['now']
        self.assertEqual(con1, con2)
