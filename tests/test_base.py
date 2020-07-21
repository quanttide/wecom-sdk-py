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

    def test_refresh_access_token(self):
        """
        刷新access_token的逻辑内置在request_api方法中，检测42001错误码删除缓存
        企业微信服务器在生成access_token以后会缓存，验证30分钟过期以后的处理十分困难
        TODO: 实现刷新access_token逻辑的测试
        :return:
        """
        self.assertTrue(True, False)


if __name__ == '__main__':
    unittest.main()
