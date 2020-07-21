# -*- coding: utf-8 -*-


class WeChatWorkSDKException(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return "WeChatWorkSDK Error {errcode}: {errmsg}".format(errcode=self.errcode, errmsg=self.errmsg)
