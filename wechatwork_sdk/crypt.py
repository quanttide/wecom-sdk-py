# -*- coding: utf-8 -*-

import re
import time
import hashlib
import base64
import socket
import struct
import string
import random

import xmltodict

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .exception import WeChatWorkSDKException


# ----- 工具函数 -----

def gen_random_str(length: int) -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


# ----- 客户端数据解密算法 -----

def extract_encrypt(xml_text: str) -> str:
    """
    解析XML中的Encrypt
    :param xml_text:
    :return:
    """
    data = xmltodict.parse(xml_text)['xml']
    return data["Encrypt"]


def cal_encrypt_sign(token: str, timestamp: str, nonce: str, encrypt: str):
    """
    计算签名
    :return:
    """
    # token、timestamp、nonce、msg_encrypt 这四个参数按照字典序排序，拼接为一个字符串
    # hashlib要求b''，必须要encode
    sort_str = "".join(sorted([token, timestamp, nonce, encrypt])).encode()
    # 用sha1算法计算签名
    sha1 = hashlib.sha1()
    sha1.update(sort_str)
    return sha1.hexdigest()


def aes_decrypt(msg_encrypt: str, encoding_aes_key: str) -> str:
    """
    AES算法解密信息
    """
    aes_msg = base64.b64decode(msg_encrypt)  # 对密文base64解码
    aes_key = base64.b64decode(encoding_aes_key + "=")  # EncodingAESKey转AESKey
    random_msg = AES.new(aes_key, AES.MODE_CBC, iv=aes_key[0:16]).decrypt(aes_msg)  # 使用AESKey做AES解密
    pad_num: int = random_msg[-1]  # 去掉补位字符串
    return random_msg[:-pad_num].decode()


def parse_random_msg(random_msg: str) -> dict:
    """
    解析随机字符串
    """
    # 规则：and_msg = random(16B) + msg_len(4B) + msg + receive_id
    content = random_msg[16:]  # 去掉前16随机字节
    xml_len: int = socket.ntohl(struct.unpack("I", content[: 4].encode())[0])
    msg = content[4: xml_len + 4]  # 截取msg_len 长度的msg
    receive_id = content[xml_len + 4:]  # 剩余字节为receive_id

    # 解析XML明文信息
    data = xmltodict.parse(msg)['xml']
    if data['ToUserName'] != receive_id:
        raise WeChatWorkSDKException("XML数据解密或明文解析错误")
    return dict(data)


def decrypt_msg(xml_text: str, encrypt_sign: str, timestamp: str, nonce: str, token: str, encoding_aes_key: str) -> dict:
    """
    解密客户端消息
    :return:
    """
    # 读取加密信息
    msg_encrypt = extract_encrypt(xml_text=xml_text)
    # 效验签名
    dev_encrypt_sign = cal_encrypt_sign(token, timestamp, nonce, msg_encrypt)
    if dev_encrypt_sign != encrypt_sign:
        raise WeChatWorkSDKException("签名效验不通过")
    # AES算法解密
    random_msg = aes_decrypt(msg_encrypt, encoding_aes_key)
    # 解析随机字符串并把XML数据转成字典
    data = parse_random_msg(random_msg)
    return data


# ----- 服务端数据加密算法 ------

def dict_to_xml(data: dict) -> str:
    xml_str = "<xml>"
    for key, value in data.items():
        pattern = re.compile(r'\d+')
        if not pattern.match(value):
            value = "<![CDATA[{value}]]>".format(value=value)
        xml_item = "<{key}>{value}</{key}>\n".format(key=key, value=value)
        xml_str += xml_item
    xml_str += "</xml>"
    return xml_str


def gen_random_msg(data: dict, random_str_16=None) -> str:
    """
    生成随机字符串
    :param data:
    :param random_str_16: 16位占位符，默认自动生成
    :return: b''
    """
    if random_str_16 is None:
        random_str_16 = gen_random_str(16)
    msg: str = dict_to_xml(data)
    random_msg = random_str_16 + struct.pack("I", socket.htonl(len(msg))).decode() + msg + data['ToUserName']
    return random_msg


def aes_encrypt(random_str: str, encoding_aes_key: str) -> str:
    aes_key = base64.b64decode(encoding_aes_key + "=")  # EncodingAESKey转AESKey
    msg_encrypt = AES.new(aes_key, AES.MODE_CBC, iv=aes_key[0:16]).encrypt(pad(random_str.encode(), 32))  # AES算法加密
    return base64.b64encode(msg_encrypt).decode()


def gen_xml_text(msg_encrypt: str, signature: str, timestamp: str, nonce: str) -> str:
    """
    生成用于发送消息的XML
    :param msg_encrypt:
    :param signature:
    :param timestamp:
    :param nonce:
    :return:
    """
    xml_text = """<xml>
    <Encrypt><![CDATA[{msg_encrypt}]]></Encrypt>
    <MsgSignature><![CDATA[{msg_signature}]]></MsgSignature>
    <TimeStamp>{timestamp}</TimeStamp>
    <Nonce><![CDATA[{nonce}]]></Nonce>
    </xml>""".format(msg_encrypt=msg_encrypt, msg_signature=signature,
                     timestamp=timestamp, nonce=nonce).replace('\n', '').replace('\r', '').replace(' ','')
    return xml_text


def encrypt_msg(data: dict, token: str, encoding_aes_key: str, timestamp=None, nonce=None, random_str_16=None) -> str:
    """
    加密需要发给客户端的消息
    :return:
    """
    if timestamp is None:
        timestamp = str(int(time.time()))
    if nonce is None:
        nonce = gen_random_str(10)  # 不确定随机字符串的要求，按照文档的位数给了10位

    # 加密数据
    random_msg: str = gen_random_msg(data, random_str_16=random_str_16)
    msg_encrypt = aes_encrypt(random_msg, encoding_aes_key)

    # 计算签名
    msg_sign = cal_encrypt_sign(token, timestamp, nonce, msg_encrypt)

    # 生成最终加密XML数据
    return gen_xml_text(msg_encrypt, msg_sign, timestamp, nonce)
