# -*- coding: utf-8 -*-
"""
身份认证服务端API

流程说明的官方文档：
  - 网页授权登录：https://work.weixin.qq.com/api/doc/90000/90135/91020
  - 扫码授权登录：https://work.weixin.qq.com/api/doc/90000/90135/90988
"""

from wecom_sdk.base.client import WeComBaseAPIClient


class WeComAuthAPIClient(WeComBaseAPIClient):
    """
    OAuth2用户认证API。

    根据文档说明，此API既可以认证企业成员，也可以认证外部成员，
    因此可能需要分别传入通讯录Secret和外部通讯录Secret。
    """
    def get_userinfo_with_auth_code(self, code):
        return self.get_api('user/getuserinfo', query_params={'code': code})


def get_wecom_userinfo_with_auth_code(corpid, secret, code):
    auth_client = WeComAuthAPIClient(corpid, secret)
    return auth_client.get_userinfo_with_auth_code(code)
