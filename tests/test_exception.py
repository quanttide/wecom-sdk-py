# -*- coding: utf-8 -*-

import unittest

from wecom_sdk.base.exception import WeComSDKException


class WeComSDKExceptionTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.sdk_exception = WeComSDKException('40001', '不合法的secret参数')

    def test_init(self):
        self.assertEqual(self.sdk_exception.errcode, '40001')

    def test_print(self):
        print(self.sdk_exception)
        self.assertEqual('\nError 40001: 不合法的secret参数', self.sdk_exception.__str__())


if __name__ == '__main__':
    unittest.main()
