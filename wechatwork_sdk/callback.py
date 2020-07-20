# -*- coding: utf-8 -*-

from .crypt import encrypt_msg, decrypt_msg


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