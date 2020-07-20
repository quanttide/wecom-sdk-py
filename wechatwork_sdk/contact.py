# -*- coding: utf-8 -*-

from .base import WeChatWorkSDK


class UserSDK(WeChatWorkSDK):
    def __init__(self, corpid, contact_secret):
        super().__init__(corpid, contact_secret)
        self._api_root_url = self._api_root_url + 'user/'

    def create(self):
        return self.post_api(api='create')

    def get(self, userid):
        return self.get_api(api='get', query_params={'userid': userid})

    def update(self):
        return self.post_api(api='update')


class DepartmentSDK(WeChatWorkSDK):
    def __init__(self, corpid, contact_secret):
        super().__init__(corpid, contact_secret)
        self._api_root_url = self._api_root_url + 'department/'

    def create(self):
        pass