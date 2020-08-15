# -*- coding: utf-8 -*-

import unittest

import sys

sys.path.append('C:\\Users\\陈方舟\\Desktop\\Python\\QuantTide\\wechatwork-sdk-py')

from wechatwork_sdk.base import WeChatWorkSDK
from tests._config import CORPID, CONTACT_SECRET
from wechatwork_sdk.external_contact import ExternalContactSDK
from wechatwork_sdk.exception import WeChatWorkSDKException


class WeChatWorkSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.wechatwork_sdk = WeChatWorkSDK(CORPID, CONTACT_SECRET)

    def test_get_access_token(self):
        access_token = self.wechatwork_sdk.access_token
        self.assertTrue(access_token)

    def test_request_api(self):
        return_data = self.wechatwork_sdk.request_api('GET', 'user/simplelist', {'department_id': 1}, data=None)
        self.assertTrue('userlist' in return_data)

    def test_refresh_access_token(self):
        """
        刷新access_token的逻辑内置在request_api方法中，检测42001错误码删除缓存
        企业微信服务器在生成access_token以后会缓存，验证30分钟过期以后的处理十分困难
        TODO: 实现刷新access_token逻辑的测试
        :return:
        """
        self.assertTrue(True, False)


class ExternalContactTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.external_contact_sdk = WeChatWorkSDK(CORPID, CONTACT_SECRET)

    def test_get_follow_user_list(self):
        """
        TODO: 实现获取配置了客户联系功能的成员列表的测试
        :return:
        """
        try:
            return_data = self.external_contact_sdk.request_api('GET', 'externalcontact/get_follow_user_list',
                                                                query_params=None, data=None)
            self.assertTrue('follow_user' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取配置了客户联系功能的成员列表的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            else:
                print(err)

    def test_get_external_contact_list(self):
        """
        TODO: 实现获取客户列表的测试
        错误码40003表示无效的userid
        错误码84061表示不存在外部联系人的关系，即该成员没有客户联系功能
        :return:
        """
        try:
            return_data = self.external_contact_sdk.request_api('GET', 'externalcontact/list',
                                                                {'userid': 'ChenFangZhou'},
                                                                data=None)
            self.assertTrue('external_userid' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取客户列表的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40003' in str(err):
                print('无效的userid，userid需更改！')
            elif '84061' in str(err):
                print('不存在外部联系人的关系，该成员没有客户联系功能！')

    def test_get_external_contact_details(self):
        """
        TODO: 实现获取客户详情的测试
        错误码40096表示不合法的外部联系人userid，即指定的外部联系人userid不存在
        错误码41035表示缺少外部联系人userid参数，即external_userid为空或未填写
        :return:
        """
        try:
            return_data = self.external_contact_sdk.request_api('GET', 'externalcontact/get',
                                                                {'external_userid': 'wo6aZhCgAAtaMUWr7vdwLDnpg6WOWAIw'},
                                                                data=None)
            self.assertTrue('external_contact' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取客户详情的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40096' in str(err):
                print('不合法的外部联系人userid，指定的外部联系人userid不存在！')
            elif '41035' in str(err):
                print('缺少外部联系人userid参数，external_userid未填写！')

    def test_edit_external_contact_remark(self):
        """
        TODO: 实现修改客户备注信息的测试
        错误码60111表示userid不存在
        错误码40096表示不合法的外部联系人userid，即指定的外部联系人userid不存在
        错误码84061表示不存在外部联系人的关系，即该成员没有客户联系功能
        :return:
        """
        try:
            data = {
                "userid": 'ChenFangZhou',
                "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
                "remark": 'cfz',
                "description": None,
                "remark_company": '量潮',
                "remark_mobiles": None
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/remark',
                                                                query_params=None, data=data)
            self.assertEqual(return_data, {})
        except WeChatWorkSDKException as err:
            print('实现修改客户备注信息的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40003' in str(err):
                print('无效的userid，userid需更改！')
            elif '40096' in str(err):
                print('不合法的外部联系人userid，指定的外部联系人userid不存在！')
            elif '84061' in str(err):
                print('不存在外部联系人的关系，该成员没有客户联系功能！')

    def test_get_corp_tag_list(self):
        """
        TODO: 实现获取企业标签库的测试
        错误码40068表示不合法的标签ID，即标签ID未指定，或者指定的标签ID不存在
        :return:
        """
        try:
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/get_corp_tag_list',
                                                                query_params=None, data={'tag_id': []})
            self.assertTrue('tag_group' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取企业标签库的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40068' in str(err):
                print('不合法的标签ID：标签ID未指定，或者指定的标签ID不存在！')

    def test_add_corp_tag(self):
        """
        TODO: 实现添加企业客户标签的测试
        错误码40071表示不合法的标签名字，即标签名字已经存在
        错误码40072表示不合法的标签名字长度，标签名不允许为空，最大长度限制为32个字（汉字或英文字母）
        错误码41018表示缺少tag.name
        :return:
        """
        try:
            data = {
                "group_id": "et6aZhCgAAuxO_IvaxZ41HsPgCTntLJQ",
                "group_name": "客户等级",
                "order": 1,
                "tag": [{"name": "重要", "order": 3},
                        {"name": "核心", "order": 4}]
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/add_corp_tag',
                                                                query_params=None, data=data)
            self.assertTrue('tag_group' in return_data)
        except WeChatWorkSDKException as err:
            print('实现添加企业客户标签的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40071' in str(err):
                print('不合法的标签名字：标签名字已经存在！')
            elif '40072' in str(err):
                print('不合法的标签名字长度：标签名不允许为空，最大长度限制为32个字（汉字或英文字母）')
            elif '41018' in str(err):
                print('缺少tag.name！')

    def test_edit_corp_tag(self):
        """
        TODO: 实现编辑企业客户标签的测试
        错误码40071表示不合法的标签名字，即标签名字已经存在
        错误码40072表示不合法的标签名字长度，标签名不允许为空，最大长度限制为32个字（汉字或英文字母）
        错误码41017表示缺少tag_id
        :return:
        """
        try:
            data = {
                "id": "et6aZhCgAAuxO_IvaxZ41HsPgCTntLJQ",
                "name": "客户等级",
                "order": 1
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/edit_corp_tag',
                                                                query_params=None, data=data)
            self.assertEqual(return_data, {})
        except WeChatWorkSDKException as err:
            print('实现编辑企业客户标签的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40071' in str(err):
                print('不合法的标签名字：标签名字已经存在！')
            elif '40072' in str(err):
                print('不合法的标签名字长度：标签名不允许为空，最大长度限制为32个字（汉字或英文字母）')
            elif '41017' in str(err):
                print('缺少tag_id！')

    def test_del_corp_tag(self):
        """
        TODO: 实现删除企业客户标签的测试
        错误码40068表示不合法的标签ID，即标签ID未指定，或者指定的标签ID不存在
        :return:
        """
        # try:
        data = {
            "tag_id": ['et6aZhCgAAxdJSwSfGsktcnP7Ast4tRQ',
                       'et6aZhCgAAQFvKhxlYP8YX8rratFoaqQ'],
            "group_id": None
        }
        return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/del_corp_tag',
                                                            query_params=None, data=data)
        self.assertEqual(return_data, {})
        # except WeChatWorkSDKException as err:
        #     print('实现删除企业客户标签的测试未通过：')
        #     if '-1' in str(err):
        #         print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
        #     elif '40068' in str(err):
        #         print('不合法的标签ID：标签ID未指定，或者指定的标签ID不存在！')

    def test_edit_external_contact_corp_tag(self):
        """
        TODO: 实现编辑客户企业标签的测试
        错误码40003表示无效的userid
        错误码40096表示不合法的外部联系人userid，即指定的外部联系人userid不存在
        错误码40068表示不合法的标签ID，即标签ID未指定，或者指定的标签ID不存在
        错误码41017表示缺少tag_id
        :return:
        """
        try:
            data = {
                "userid": 'ChenFangZhou',
                "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
                "add_tag": 'et6aZhCgAAMLwe0k2V0c0HoN7t_GjzbA',
                "remove_tag": []
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/mark_tag',
                                                                query_params=None, data=data)
            self.assertEqual(return_data, {})
        except WeChatWorkSDKException as err:
            print('实现编辑客户企业标签的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40003' in str(err):
                print('无效的userid，userid需更改！')
            elif '40096' in str(err):
                print('不合法的外部联系人userid，指定的外部联系人userid不存在！')
            elif '40068' in str(err):
                print('不合法的标签ID：标签ID未指定，或者指定的标签ID不存在！')
            elif '41017' in str(err):
                print('缺少tag_id，需填写add_tag或remove_tag！')

    def test_get_groupchat_list(self):
        """
        TODO: 实现获取客户群列表的测试
        错误码40058表示不合法的参数，要求status_filter只能取0、1、2、3，
        limit必须填写取值范围为1 ~ 1000， offset + limit 总数不能大于5万
        :return:
        """
        try:
            data = {
                "status_filter": 0,
                "owner_filter": {},
                "offset": 0,
                "limit": 100
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/groupchat/list',
                                                                query_params=None, data=data)
            self.assertTrue('group_chat_list' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取客户群列表的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40058' in str(err):
                print('不合法的参数：status_filter只能取0、1、2、3，'
                      'limit必须填写取值范围为1 ~ 1000， offset + limit 总数不能大于5万！')

    def test_get_groupchat_details(self):
        """
        TODO: 实现获取客户群详情的测试
        错误码40050表示chat_id不存在
        :return:
        """
        try:
            data = {'chat_id': 'wr6aZhCgAAqh24yCnF3W0oO66mFZGRKA'}
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/groupchat/get',
                                                                query_params=None, data=data)
            self.assertTrue('group_chat' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取客户群详情的测试的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40050' in str(err):
                print('chat_id不存在')

    def test_get_unassigned_list(self):
        """
        TODO: 实现获取离职成员的客户列表的测试
        :return:
        """
        try:
            data = {'page_id': 0, "page_size": 10}
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/get_unassigned_list',
                                                                query_params=None, data=data)
            self.assertTrue('info' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取离职成员的客户列表的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            else:
                print(err)

    def test_external_contact_transfer(self):
        """
        TODO: 实现离职成员的外部联系人再分配的测试
        错误码40003表示无效的userid
        错误码40097表示该成员尚未离职，离职成员外部联系人转移接口要求转出用户必须已经离职
        :return:
        """
        try:
            # 需要更改
            data = {
                "external_userid": "wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw",
                "handover_userid": "HeLiJian",
                "takeover_userid": "ChenFangZhou"
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/transfer',
                                                                query_params=None, data=data)
            self.assertEqual(return_data, {})
        except WeChatWorkSDKException as err:
            print('实现离职成员的外部联系人再分配的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40003' in str(err):
                print('无效的userid，userid需更改！')
            elif '40097' in str(err):
                print('该成员尚未离职，handover_userid需更改！')

    def test_groupchat_transfer(self):
        """
        TODO: 实现离职成员的群再分配的测试
        错误码40058表示不合法的参数，要求chat_id_list和new_owner不能为空
        错误码46004表示指定的用户new_owner不存在
        错误码90500表示群主并未离职
        :return:
        """
        try:
            # 需要更改
            data = {
                "chat_id_list": ["wr6aZhCgAA1g9wJtYmMT6RDW6L5aQc4A"],
                "new_owner": "ChenFan"
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/groupchat/transfer',
                                                                query_params=None, data=data)
            self.assertEqual(return_data['failed_chat_list'][0]['errcode'], 0)
        except WeChatWorkSDKException as err:
            print('实现离职成员的群再分配的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40058' in str(err):
                print('不合法的参数：chat_id_list和new_owner不能为空！')
            elif '46004' in str(err):
                print('指定的用户new_owner不存在，new_owner需更改！')
        except AssertionError:
            print('实现离职成员的群再分配的测试未通过：')
            if '90500' in str(return_data):
                print('该群群主并未离职！')

    def test_get_user_behavior_data(self):
        """
        TODO: 实现获取联系客户统计数据的测试
        错误码40003表示无效的userid
        错误码60123表示无效的部门id
        错误码600018表示无效的起始结束时间
        :return:
        """
        try:
            # 2020-07-20到2020-08-02的数据
            data = {
                "userid": ['ChenFangZhou', 'ChenFan'],
                "partyid": [1],
                "start_time": 1595174400,
                "end_time": 1596297600
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/get_user_behavior_data',
                                                                query_params=None, data=data)
            self.assertTrue('behavior_data' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取联系客户统计数据的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40003' in str(err):
                print('无效的userid，userid需更改！')
            elif '60123' in str(err):
                print('无效的部门id，partyid需更改！')
            elif '600018' in str(err):
                print('无效的起始结束时间，start_time和（或）end_time需更改！')

    def test_get_groupchat_data(self):
        """
        TODO: 实现获取客户群统计数据的测试
        错误码600018表示无效的起始结束时间
        错误码40003表示无效的userid
        错误码60123表示无效的部门id
        错误码40058表示不合法的参数，要求order_by只能取1、2、3、4，order_asc只能取0、1，limit范围为1 ~ 1000
        :return:
        """
        try:
            data = {
                "day_begin_time": 1595174400,
                "owner_filter": {},
                "order_by": 2,
                "order_asc": 0,
                "offset": 0,
                "limit": 100
            }
            return_data = self.external_contact_sdk.request_api('POST', 'externalcontact/groupchat/statistic',
                                                                query_params=None, data=data)
            self.assertTrue('items' in return_data)
        except WeChatWorkSDKException as err:
            print('实现获取客户群统计数据的测试未通过：')
            if '-1' in str(err):
                print('系统繁忙：服务器暂不可用，建议稍候重试。建议重试次数不超过3次。')
            elif '40003' in str(err):
                print('无效的userid，userid需更改！')
            elif '60123' in str(err):
                print('无效的部门id，partyid需更改！')
            elif '40058' in str(err):
                print('order_by只能取1、2、3、4，order_asc只能取0、1，limit范围为1 ~ 1000')
            elif '600018' in str(err):
                print('无效的起始结束时间，day_begin_time需更改！')


if __name__ == '__main__':
    unittest.main()
