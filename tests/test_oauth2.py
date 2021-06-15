# -*- coding: utf-8 -*-

import unittest
import os

from wecom_sdk.base.exception import WeComSDKException
from wecom_sdk.oauth2 import WeComAuthAPIClient


# ----- 环境变量读取密钥 -----
from environs import Env
Env().read_env()

CORPID = os.environ.get('CORPID')
CONTACT_SECRET = os.environ.get('CONTACT_SECRET')
EXTERNAL_CONTACT_SECRET = os.environ.get('EXTERNAL_CONTACT_SECRET')


# ----- 单元测试用例 -----

class WeComAuthAPIClientTestCase(unittest.TestCase):
    contact_client = WeComAuthAPIClient(CORPID, CONTACT_SECRET)
    external_contact_client = WeComAuthAPIClient(CORPID, EXTERNAL_CONTACT_SECRET)

    def test_user_auth_with_invalid_code(self):
        invalid_code = 'gegwgessege'
        with self.assertRaises(WeComSDKException) as e:
            self.contact_client.get_userinfo_with_auth_code(invalid_code)
        self.assertEqual(e.exception.errcode, '40029')

    def test_external_user_auth_with_invalid_code(self):
        invalid_code = 'gegwgessege'
        with self.assertRaises(WeComSDKException) as e:
            self.external_contact_client.get_userinfo_with_auth_code(invalid_code)
        self.assertEqual(e.exception.errcode, '40029')


if __name__ == '__main__':
    unittest.main()
