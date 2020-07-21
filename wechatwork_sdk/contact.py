# -*- coding: utf-8 -*-

from .base import WeChatWorkSDK


class UserSDK(WeChatWorkSDK):
    def __init__(self, corpid, contact_secret):
        super().__init__(corpid, contact_secret)
        self._api_root_url = self._api_root_url + 'user/'

    def create(self, userid, name, **kwargs):
        pass

    def get(self, userid):
        """
        读取成员
        :param userid: 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。
        :return:
        """
        return self.get_api(api='get', query_params={'userid': userid})


class DepartmentSDK(WeChatWorkSDK):
    def __init__(self, corpid, contact_secret):
        super().__init__(corpid, contact_secret)
        self._api_root_url = self._api_root_url + 'department/'
