# -*- coding: utf-8 -*-


class WeComSDKException(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = str(errcode)
        self.errmsg = errmsg

    def __str__(self):
        return "\nError {errcode}: {errmsg}".format(errcode=self.errcode, errmsg=self.errmsg)
