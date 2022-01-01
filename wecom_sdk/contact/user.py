# -*- coding: utf-8 -*-


class UserAPIMixin(object):
    """
    成员管理API
    """
    # --- 通用API ---
    def request_user_api(self, method, api, query_params=None, data=None):
        api = 'user/' + api
        return self.request_api(method, api, query_params, data)

    def get_user_api(self, api, query_params=None, data=None):
        return self.request_user_api('GET', api, query_params, data)

    def post_user_api(self, api, query_params=None, data=None):
        return self.request_user_api('POST', api, query_params, data)

    # --- API ---
    def create_user(self, userid, name, **kwargs):
        pass

    def get_user(self, userid):
        """
        读取成员
        :param userid: 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。
        :return:
        """
        return self.get_user_api(api='get', query_params={'userid': userid})

    def get_user_simple_list(self, department_id, fetch_child=1):
        """

        """
        return self.get_user_api(api='simplelist', query_params={'department_id': department_id,
                                                                 "fetch_child": fetch_child})['userlist']

    def get_user_list(self, department_id, fetch_child=1):
        return self.get_user_api(api='list', query_params={'department_id': department_id,
                                                           "fetch_child": fetch_child})['userlist']

    # --- high level API ---
    def get_user_list_of_all(self, simple_list=True):
        """
        获取本企业下所有用户
        """
        if simple_list:
            return self.get_user_simple_list(department_id=1, fetch_child=1)
        else:
            return self.get_user_list(department_id=1, fetch_child=1)
