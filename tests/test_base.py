# -*- coding: utf-8 -*-

import unittest

from wechatwork_sdk.base import WeChatWorkSDK
from ._config import CORPID, CONTACT_SECRET


class WeChatWorkSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.wechatwork_sdk = WeChatWorkSDK(CORPID, CONTACT_SECRET)

    def test_get_access_token(self):
        access_token = self.wechatwork_sdk.access_token
        self.assertTrue(access_token)

    def test_request_api(self):
        return_data = self.wechatwork_sdk.request_api('GET', 'user/simplelist', {'department_id': 1})
        self.assertTrue('userlist' in return_data)


if __name__ == '__main__':
    unittest.main()
