# -*- coding: utf-8 -*-

from .base import WeChatWorkSDK


class UserSDK(WeChatWorkSDK):
    API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'user/'

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
    API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'department/'

