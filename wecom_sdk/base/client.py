# -*- coding: utf-8 -*-


import json

import requests

from wecom_sdk.base.exception import WeChatWorkSDKException
from wecom_sdk.common.mixin import ValidationMixin


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
        raise WeChatWorkSDKException(data['errcode'], data['errmsg'])


class WeChatWorkSDK(ValidationMixin):
    """
    企业微信SDK基本类
    """
    API_ROOT_URL = WECHATWORK_API_ROOT_URL

    def __init__(self, corpid, secret):
        """
        :param corpid:
        :param secret:
        """
        self.corpid = corpid
        self.secret = secret
        self._access_token = None

    @property
    def access_token(self):
        """
        获取access_token
        详细说明：https://work.weixin.qq.com/api/doc/90000/90135/91039

        :return access_token: str
        """
        # 新创建的实例或者access_token过期，请求access_token并缓存
        if self._access_token is None:
            access_token, expires_in = get_access_token(corpid=self.corpid, secret=self.secret)
            self._access_token = access_token
        return self._access_token

    def _clean_cached_access_token(self):
        self._access_token = None

    def request_api(self, method, api, query_params=None, data=None):
        # 验证数据
        self.validate(**{**query_params, **data})

        # 拼接API的URL
        url = self.API_ROOT_URL + api

        # 默认必须传入access_token
        if query_params is None:
            query_params = dict()
        query_params['access_token'] = self.access_token

        # API接口要求必须以JSON格式传入数据
        content = requests.request(method, url, params=query_params, json=data).content
        if not content:
            raise WeChatWorkSDKException('self-defined', 'API接口不存在')
        return_data = json.loads(content)

        # 处理access_token过期
        if int(return_data['errcode']) == 42001:
            # 清空缓存的access_token
            self._clean_cached_access_token()
            # 重新请求
            return self.request_api(method, api, query_params, data)

        # 抛出异常
        if int(return_data['errcode']) != 0:
            raise WeChatWorkSDKException(return_data['errcode'], return_data['errmsg'])

        # 返回正常数据时删除errcode=0和errmsg='ok'
        return_data.pop('errcode')
        return_data.pop('errmsg')
        return return_data

    def get_api(self, api, query_params=None):
        return self.request_api('GET', api, query_params)

    def post_api(self, api, query_params=None, data=None):
        return self.request_api('POST', api, query_params, data)



