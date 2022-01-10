from django.test import TestCase
from unittest import mock
from django.shortcuts import resolve_url
from django.urls import reverse

import datetime as dt

from icecream import ic

from dotenv import load_dotenv
load_dotenv()


class IndexTest(TestCase):
    def test_index_output(self):

        # compare screen displays
        res = self.client.get(reverse('display_part:index_old'))
        res_as_view = self.client.get(reverse('display_part:index'))
        self.assertEqual(res.content, res_as_view.content)

        # compare contexts
        con1 = dict(res.context)
        con2 = dict(res_as_view.context)
        exclude_keylist = ['csrf_token', 'messages', 'perms', 'view', 'request']
        con1 = {k: v for k, v in con1.items() if k not in exclude_keylist}
        con2 = {k: v for k, v in con2.items() if k not in exclude_keylist}
        self.assertEqual(con1, con2)
