# -*- coding: utf-8 -*-

import unittest
import os

from wecom_sdk.contact import UserAPIClient


from environs import Env
Env().read_env()

CORPID = os.environ.get('CORPID')
CONTACT_SECRET = os.environ.get('CONTACT_SECRET')
USER_ID = os.environ.get('USER_ID')


class UserAPIClientTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.contact_client = UserAPIClient(CORPID, CONTACT_SECRET)

    def test_get_user(self):
        self.contact_client.get_user(userid=USER_ID)


if __name__ == "__main__":
    unittest.main()