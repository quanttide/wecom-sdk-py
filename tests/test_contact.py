# -*- coding: utf-8 -*-

import unittest
import os

from wecom_sdk.contact import WecomContactAPIClient


from environs import Env
Env().read_env()

CORPID = os.environ.get('CORPID')
CONTACT_SECRET = os.environ.get('CONTACT_SECRET')


class UserAPIClientTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.contact_client = WecomContactAPIClient(CORPID, CONTACT_SECRET)

    def test_get_user(self):
        user_id = os.environ.get('TEST_USER_ID')
        self.contact_client.get_user(userid=user_id)

    def test_get_user_list_of_all(self):
        data = self.contact_client.get_user_list_of_all()
        self.assertTrue(data)


class TagAPIClientTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.contact_client = WecomContactAPIClient(CORPID, CONTACT_SECRET)
        cls.tag_id = os.environ.get('TEST_TAG_ID')
        cls.tag_name = os.environ.get('TEST_TAG_NAME')

    def test_get_members_by_tag_id(self):
        self.contact_client.get_members_by_tag_id(self.tag_id)

    def test_find_tag_id_by_name(self):
        tag_id = self.contact_client.find_tag_id_by_name(self.tag_name)
        self.assertTrue(tag_id)

    def test_get_members_by_tag_name(self):
        data = self.contact_client.get_members_by_tag_name(self.tag_name)
        self.assertTrue('userlist' in data)
        self.assertTrue('partylist' in data)


if __name__ == "__main__":
    unittest.main()
