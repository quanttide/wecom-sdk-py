# -*- coding: utf-8 -*-

import unittest
import os

from wecom_sdk.base.client import WeComBaseAPIClient


# 环境变量读取密钥配置
from environs import Env
Env().read_env()

CORPID = os.environ.get('CORPID')
CONTACT_SECRET = os.environ.get('CONTACT_SECRET')


class WeComBaseAPIClientTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.client = WeComBaseAPIClient(CORPID, CONTACT_SECRET)

    def test_get_access_token(self):
        access_token = self.client.access_token
        self.assertTrue(access_token)

    def test_request_api(self):
        return_data = self.client.request_api('GET', 'user/simplelist', {'department_id': 1})
        self.assertTrue('userlist' in return_data)


if __name__ == '__main__':
    unittest.main()
