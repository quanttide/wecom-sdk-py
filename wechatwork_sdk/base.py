# -*- coding: utf-8 -*-


import json

import requests

from .exception import WeChatWorkSDKException


# 企业微信API根URL
WECHATWORK_API_ROOT_URL = 'https://qyapi.weixin.qq.com/cgi-bin/'


def get_access_token(corpid, secret) -> (str, int):
    """
    获取Access Token
    :param corpid: 企业ID
    :param secret: 应用密钥
    :return: (access_token, expires_in)
        - access_token: 获取到的凭证，最长为512字节
        - expires_in: 凭证的有效时间（秒），通常为7200
    """
    url = WECHATWORK_API_ROOT_URL + 'gettoken?corpid={corpid}&corpsecret={secret}'\
        .format(corpid=corpid, secret=secret)
    data = json.loads(requests.get(url).content)
    if int(data['errcode']) == 0:
        return data['access_token'], int(data['expires_in'])
    else:
        raise WeChatWorkSDKException(data)


class WeChatWorkSDK(object):
    """
    企业微信SDK基本类
    """
    def __init__(self, corpid, secret):
        """
        :param corpid:
        :param secret:
        :param name: 自定义的名称
        """
        self.corpid = corpid
        self.secret = secret
        self._api_root_url = WECHATWORK_API_ROOT_URL

    @property
    def access_token(self):
        """
        获取access_token
        详细说明：https://work.weixin.qq.com/api/doc/90000/90135/91039

        :return access_token: str
        """
        access_token, expires_in = get_access_token(corpid=self.corpid, secret=self.secret)
        return access_token

    def request_api(self, method, api, query_params=None, data=None):
        url = self._api_root_url + api

        # 默认必须传入access_token
        if query_params is None:
            query_params = dict()
        query_params['access_token'] = self.access_token

        # API接口要求必须以JSON格式传入数据
        response = requests.request(method, url, params=query_params, json=data)
        return_data = json.loads(response.content)

        # 抛出异常
        if return_data['errcode'] != 0:
            raise WeChatWorkSDKException(return_data)

        # 返回时删除errcode和errmsg
        return_data.pop('errcode')
        return_data.pop('errmsg')
        return return_data

    def get_api(self, api, query_params=None):
        return self.request_api('GET', api, query_params)

    def post_api(self, api, query_params=None, data=None):
        return self.request_api('POST', api, query_params, data)



