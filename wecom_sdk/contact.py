# -*- coding: utf-8 -*-

from wecom_sdk.base.client import WeComBaseAPIClient
from wecom_sdk.oauth2 import WeComAuthAPIClient


class UserAPIClient(WeComAuthAPIClient):
    """
    成员管理API
    """
    def request_user_api(self, method, api, query_params=None, data=None):
        api = 'user/' + api
        return self.request_api(method, api, query_params, data)

    def get_user_api(self, api, query_params=None, data=None):
        return self.request_user_api('GET', api, query_params, data)

    def post_user_api(self, api, query_params=None, data=None):
        return self.request_user_api('POST', api, query_params, data)

    def create_user(self, userid, name, **kwargs):
        pass

    def get_user(self, userid):
        """
        读取成员
        :param userid: 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。
        :return:
        """
        return self.get_user_api(api='get', query_params={'userid': userid})


class DepartmentAPIClient(WeComBaseAPIClient):
    pass

