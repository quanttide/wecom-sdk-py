# -*- coding: utf-8 -*-


def get_access_token(corpid, secret) -> (str, int):
    """
    获取Access Token
    :param corpid: 企业ID
    :param secret: 应用密钥
    :return:
    """
    url = WECHATWORK_API_ROOT_URL + 'gettoken?corpid={corpid}&corpsecret={secret}'\
        .format(corpid=corpid, secret=secret)
    data = json.loads(requests.get(url).content)
    if int(data['errcode']) == 0:
        return data['access_token'], int(data['expires_in'])
    else:
        raise WeChatWorkSDKException(data['errmsg'])


class WeChatWorkSDK(object):
    """
    企业微信SDK基本类
    """
    def __init__(self, corpid=None, secret=None, name=None):
        """
        :param corpid:
        :param secret:
        :param name: 自定义的名称
        """
        self.name = name
        if self.name is not None:
            self._access_token_key = 'wechatwork_access_token_' + self.name
        else:
            self._access_token_key = 'wechatwork_access_token'
        if corpid is None:
            # 默认为Django settings传入的corpid
            corpid = CORPID
        self.corpid = corpid
        if secret is None:
            raise WeChatWorkSDKException("secret不可以为空")
        self.secret = secret
        self._api_root_url = WECHATWORK_API_ROOT_URL

    @property
    def access_token(self):
        """
        获取access_token
        详细说明：https://work.weixin.qq.com/api/doc/90000/90135/91039

        首先从缓存中获取；若缓存不存在或者过期，则通过调用接口从企业微信服务器获取并缓存
        property装饰器只是把方法变成属性，每次被调用时依然会调用方法并且返回属性，不会出现缓存过期依然被使用的情况
        :return access_token: str
        """
        try:
            access_token = cache.get(self._access_token_key)
        except KeyError:
            access_token = None

        # access_token缓存为空或者不存在此缓存数据时，都处理为None并且重新请求
        if access_token is None:
            access_token, expires_in = get_access_token(corpid=self.corpid, secret=self.secret)
            cache.set(self._access_token_key, access_token, timeout=int(expires_in))

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


class WeChatWorkCallbackSDK(object):
    """
    企业微信回调SDK基本类，用于实现内部系统和企业微信客户端的双向通信
    详细说明：https://work.weixin.qq.com/api/doc/90000/90135/90930
    """
    def __init__(self, token, encoding_aes_key):
        self.token = token
        self.encoding_aes_key = encoding_aes_key

    def encrypt(self, data: dict) -> str:
        """
        服务端加密数据
        :param data:
        :param timestamp:
        :param nonce:
        :return:
        """
        return encrypt_msg(data, token=self.token, encoding_aes_key=self.encoding_aes_key)

    def decrypt(self, xml, sign, timestamp, nonce) -> dict:
        """
        验证并解密来自客户端的数据
        :return:
        """
        return decrypt_msg(xml_text=xml, encrypt_sign=sign, timestamp=timestamp, nonce=nonce,
                           token=self.token, encoding_aes_key=self.encoding_aes_key)

