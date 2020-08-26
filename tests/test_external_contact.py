# -*- coding: utf-8 -*-

import unittest
from tests._config import CORPID, EXTERNAL_CONTACT_SECRET
from wechatwork_sdk.external_contact import ExternalContactSDK
from wechatwork_sdk.exception import WeChatWorkSDKException


class ExternalContactTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.external_contact_sdk = ExternalContactSDK(CORPID, EXTERNAL_CONTACT_SECRET)

    def test_get_follow_user_list(self):
        """
        实现获取配置了客户联系功能的成员列表的测试
        :return:
        """
        return_data = self.external_contact_sdk.get_follow_user_list()
        self.assertTrue('follow_user' in return_data)

    def test_get_external_contact_list(self):
        """
        实现获取客户列表的测试
        :return:
        """
        return_data = self.external_contact_sdk.get_external_contact_list('ChenFangZhou')
        self.assertTrue('external_userid' in return_data)

    def test_get_external_contact_list_no_userid(self):
        """
        实现获取客户列表的测试：userid为空
        :return:
        WeChatWorkSDK Error 60111: userid not found。userid参数为空。
        """
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_external_contact_list, '')

    def test_get_external_contact_list_not_external_contact(self):
        """
        实现获取客户列表的测试：该成员没有客户联系功能
        :return:
        WeChatWorkSDK Error 84061: not external contact。不存在外部联系人的关系。
        """
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_external_contact_list, 'MaYongKang')

    def test_get_external_contact_list_invalid_userid(self):
        """
        实现获取客户列表的测试：无效的userid
        :return:
        WeChatWorkSDK Error 40003: invalid userid
        """
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_external_contact_list, 'ZhangSan')

    def test_get_external_contact_details(self):
        """
        实现获取客户详情的测试
        :return:
        """
        return_data = self.external_contact_sdk.get_external_contact_details('wo6aZhCgAAtaMUWr7vdwLDnpg6WOWAIw')
        self.assertTrue('external_contact' in return_data)

    def test_get_external_contact_details_no_external_userid(self):
        """
        实现获取客户详情的测试：external_userid为空
        :return:
        WeChatWorkSDK Error 41035: missing external userid。缺少外部联系人userid参数。
        """
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_external_contact_details, '')

    def test_get_external_contact_details_invalid_external_userid(self):
        """
        实现获取客户详情的测试：指定的外部联系人userid不存在
        :return:
        WeChatWorkSDK Error 40096: invalid external userid。
        """
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_external_contact_details,
                          'ww6aZhCgAAtaMUWr7vdwLDnpg6WOWAIw')

    def test_edit_external_contact_remark(self):
        """
        实现修改客户备注信息的测试
        :return:
        """
        info = {
            "userid": 'ChenFangZhou',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "remark": 'cfz',
            "description": None,
            "remark_company": '量潮',
            "remark_mobiles": None
        }
        return_data = self.external_contact_sdk.edit_external_contact_remark(**info)
        self.assertEqual(return_data, {})

    def test_edit_external_contact_remark_invalid_userid(self):
        """
        实现修改客户备注信息的测试：无效的userid
        :return:
        WeChatWorkSDK Error 40003: invalid userid
        """
        info = {
            "userid": 'ZhangSan',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "remark_company": '量潮'
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_external_contact_remark, **info)

    def test_edit_external_contact_remark_invalid_external_userid(self):
        """
        实现修改客户备注信息的测试：指定的外部联系人userid不存在
        :return:
        WeChatWorkSDK Error 40096: invalid external userid
        """
        info = {
            "userid": 'ChenFangZhou',
            "external_userid": 'wo6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "remark_company": '量潮'
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_external_contact_remark, **info)

    def test_edit_external_contact_remark_not_external_contact(self):
        """
        实现修改客户备注信息的测试：该成员没有客户联系功能
        :return:
        WeChatWorkSDK Error 84061: not external contact。不存在外部联系人的关系。
        """
        info = {
            "userid": 'MaYongKang',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "remark_company": '量潮'
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_external_contact_remark, **info)

    def test_get_corp_tag_list(self):
        """
        实现获取企业标签库的测试
        :return:
        """
        return_data = self.external_contact_sdk.get_corp_tag_list()
        self.assertTrue('tag_group' in return_data)

    def test_get_corp_tag_list_invalid_tag(self):
        """
        实现获取企业标签库的测试：指定的标签ID不存在
        :return:
        Error 40068: Warning: wrong json format. invalid tagid
        """
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_corp_tag_list,
                          'at6aZhCgAAH_bZ-L3Q6Hn5cq-Y1jquRg')

    def test_add_corp_tag(self):
        """
        实现添加企业客户标签的测试
        :return:
        """
        data = {
            "group_id": "et6aZhCgAAcviRSOBEM8L5hw-cRQ0-sw",
            "group_name": "客户等级",
            "order": 0,
            "tag": [{"name": "VIP", "order": 3},
                    {"name": "SVIP", "order": 4}]
        }
        return_data = self.external_contact_sdk.add_corp_tag(**data)
        self.assertTrue('tag_group' in return_data)

    def test_add_corp_tag_invalid_tag_name(self):
        """
        实现添加企业客户标签的测试：不合法的标签名字，标签名字已经存在
        :return:
        WeChatWorkSDK Error 40071: UserTag Name Already Exist
        """
        data = {
            "group_id": "et6aZhCgAAcviRSOBEM8L5hw-cRQ0-sw",
            "group_name": "客户等级",
            "order": 0,
            "tag": [{"name": "核心", "order": 2}]
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.add_corp_tag, **data)

    def test_add_corp_tag_missing_tag_name(self):
        """
        实现添加企业客户标签的测试：缺少tag.name
        :return:
        WeChatWorkSDK Error 41018: missing tagname
        """
        data = {
            "group_id": "et6aZhCgAAcviRSOBEM8L5hw-cRQ0-sw",
            "group_name": "客户等级",
            "order": 0,
            "tag": [{"name": "", "order": 3}]
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.add_corp_tag, **data)

    def test_edit_corp_tag(self):
        """
        实现编辑企业客户标签的测试
        :return:
        """
        tag = {
            "id": "et6aZhCgAATEWosWn6ZSfUlFweGLkPSQ",
            "name": "核心",
            "order": 2
        }
        return_data = self.external_contact_sdk.edit_corp_tag(**tag)
        self.assertEqual(return_data, {})

    def test_edit_corp_tag_group(self):
        """
        实现编辑企业客户标签组的测试
        :return:
        """
        tag = {
            "id": "et6aZhCgAAcviRSOBEM8L5hw-cRQ0-sw",
            "name": "客户等级",
            "order": 0
        }
        return_data = self.external_contact_sdk.edit_corp_tag(**tag)
        self.assertEqual(return_data, {})

    def test_edit_corp_tag_missing_tag_id(self):
        """
        实现编辑企业客户标签的测试：缺少tag_id
        :return:
        WeChatWorkSDK Error 41017: missing tagid
        """
        tag = {
            "id": "",
            "name": "核心",
            "order": 2
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_corp_tag, **tag)

    def test_del_corp_tag(self):
        """
        实现删除企业客户标签的测试
        :return:
        """
        tag_info = self.external_contact_sdk.get_corp_tag_list()
        tag_id_list = []
        for i in range(len(tag_info['tag_group'][0]['tag'])):
            if tag_info['tag_group'][0]['tag'][i]['name'] in ['VIP', 'SVIP']:
                tag_id_list.append(tag_info['tag_group'][0]['tag'][i]['id'])
        data = {"tag_id": tag_id_list}
        return_data = self.external_contact_sdk.del_corp_tag(**data)
        self.assertEqual(return_data, {})

    def test_del_corp_tag_invalid_tag_id(self):
        """
        实现删除企业客户标签的测试：指定的标签ID不存在
        :return:
        WeChatWorkSDK Error 40068: invalid tagid
        """
        data = {
            "tag_id": ['et6aZhCgAA43cqugMD5b7JuioUwUev4w',
                       'et6aZhCgAAC0Q0ilTFV6kQa2WPSYKu6g']
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.del_corp_tag, **data)

    def test_del_corp_tag_missing_tag_id(self):
        """
        实现删除企业客户标签的测试：缺少tag_id
        :return:
        WeChatWorkSDK Error 41017: missing tagid
        """
        data = {
            "tag_id": []
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.del_corp_tag, **data)

    def test_edit_external_contact_corp_tag(self):
        """
        实现编辑客户企业标签的测试
        :return:
        """
        tag = {
            "userid": 'ChenFangZhou',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "add_tag": 'et6aZhCgAATEWosWn6ZSfUlFweGLkPSQ',
            "remove_tag": 'et6aZhCgAAlEoiGNLtxKZ6z_v7K_tIMw'
        }
        return_data = self.external_contact_sdk.edit_external_contact_corp_tag(**tag)
        self.assertEqual(return_data, {})

    def test_edit_external_contact_corp_tag_invalid_tag_id(self):
        """
        实现编辑客户企业标签的测试：指定的标签ID不存在
        :return:
        WeChatWorkSDK Error 40068: Warning: wrong json format. invalid tagid
        """
        tag = {
            "userid": 'ChenFangZhou',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "add_tag": 'et6aZhCgAASHC88CxCS1anIH9s8RepHQ',
            "remove_tag": []
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_external_contact_corp_tag, **tag)

    def test_edit_external_contact_corp_tag_missing_tag_id(self):
        """
        实现编辑客户企业标签的测试：缺少tag_id
        :return:
        WeChatWorkSDK Error 41017: missing tagid
        """
        tag = {
            "userid": 'ChenFangZhou',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "add_tag": [],
            "remove_tag": []
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_external_contact_corp_tag, **tag)

    def test_edit_external_contact_corp_tag_not_external_contact(self):
        """
        实现编辑客户企业标签的测试：不存在外部联系人的关系，即指定的外部联系人userid不存在
        :return:
        WeChatWorkSDK Error 84061: Warning: wrong json format. not external contact
        """
        tag = {
            "userid": 'MaYongKang',
            "external_userid": 'wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw',
            "add_tag": 'et6aZhCgAATEWosWn6ZSfUlFweGLkPSQ',
            "remove_tag": []
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_external_contact_corp_tag, **tag)

    def test_get_groupchat_list(self):
        """
        实现获取客户群列表的测试
        :return:
        """
        data = {
            "status_filter": 0,
            "owner_filter": {},
            "offset": 0,
            "limit": 100
        }
        return_data = self.external_contact_sdk.get_groupchat_list(**data)
        self.assertTrue('group_chat_list' in return_data)

    def test_get_groupchat_list_invalid_arg(self):
        """
        实现获取客户群列表的测试：不合法的参数
        :return:
        WeChatWorkSDK Error 40058: status_filter invalid。status_filter只能取0、1、2、3
        """
        data = {
            "status_filter": 4,
            "owner_filter": {},
            "offset": 0,
            "limit": 100
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_groupchat_list, **data)

    def test_get_groupchat_details(self):
        """
        实现获取客户群详情的测试
        :return:
        """
        data = {'chat_id': 'wr6aZhCgAAqh24yCnF3W0oO66mFZGRKA'}
        return_data = self.external_contact_sdk.get_groupchat_details(**data)
        self.assertTrue('group_chat' in return_data)

    def test_get_groupchat_details_invalid_group_id(self):
        """
        实现获取客户群详情的测试：chat_id不存在
        :return:
        WeChatWorkSDK Error 40050: invalid group id。chat_id不存在
        """
        data = {'chat_id': 'wr6aZhCgAAqh24yCnF3W0oO66mFZQc4A'}
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_groupchat_details, **data)

    def test_add_msg_template(self):
        """
        实现添加企业群发消息任务的测试
        :return:
        """
        data = {
            "external_userid": ["wo6aZhCgAAtaMUWr7vdwLDnpg6WOWAIw"],
            "sender": "ChenFangZhou",
            "text": {"content": "您好，我是量潮的陈方舟。请问有什么需要帮忙的吗？"}
        }
        return_data = self.external_contact_sdk.add_msg_template(**data)
        self.assertTrue('msgid' in return_data)
        self.assertEqual(return_data['fail_list'], [])

    def test_add_msg_template_missing_arg(self):
        """
        实现添加企业群发消息任务的测试：text、image、link和miniprogram四者不能同时为空
        :return:
        WeChatWorkSDK Error 40063: some parameters are empty
        """
        data = {
            "external_userid": ["wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw"],
            "sender": "ChenFangZhou"
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.add_msg_template, **data)

    def test_add_msg_template_no_customer_to_send(self):
        """
        实现添加企业群发消息任务的测试：无可发送的客户，即该客户被发送的消息已超过限制
        :return:
        WeChatWorkSDK Error 41048: no customer to send
        """
        data = {
            "external_userid": ["wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw"],
            "sender": "ChenFangZhou",
            "text": {"content": "您好，我是量潮的陈方舟。请问有什么需要帮忙的吗？"}
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.add_msg_template, **data)

    def test_add_msg_template_not_external_contact(self):
        """
        实现添加企业群发消息任务的测试：不存在外部联系人的关系，即指定的外部联系人userid不存在
        :return:
        WeChatWorkSDK Error 84061: not external contact。不存在外部联系人的关系。
        """
        data = {
            "external_userid": ["wm6aZhCgAAKnotxPtAz68KmVbNubRr6g"],
            "sender": "ChenFan",
            "text": {"content": "您好，请问有什么需要帮忙的吗？"}
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.add_msg_template, **data)

    def test_get_group_msg_result(self):
        """
        实现获取企业群发消息发送结果的测试
        :return:
        """
        data = {'msgid': 'msg6aZhCgAA3uWG6Ue61PkWpDvzDoqtxg'}
        return_data = self.external_contact_sdk.get_group_msg_result(**data)
        self.assertTrue('detail_list' in return_data)

    def test_get_group_msg_result_invalid_group_msg_id(self):
        """
        实现获取企业群发消息发送结果的测试：msgid错误
        :return:
        WeChatWorkSDK Error 41047: invalid group msg id。无效的企业群发消息id。
        """
        data = {'msgid': 'msgGCAAAXtWyujaWJHDDGi0mACas1w'}
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_group_msg_result, **data)

    def test_send_welcome_msg_invalid_welcome_code(self):
        """
        实现发送新客户欢迎语的测试：无效的欢迎语code
        :return:
        WeChatWorkSDK Error 41050: invalid welcome code
        """
        data = {
            "welcome_code": "CALLBACK_CODE",
            "text": {"content": "您好，这里是量潮，很高兴为您服务！"}
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.send_welcome_msg, **data)

    def test_add_and_del_group_welcome_template(self):
        """
        实现添加群欢迎语素材和删除群欢迎语素材的测试
        :return:
        """
        data = {
            "text": {"content": "您好，这里是量潮，很高兴为您服务！"}
        }
        return_data = self.external_contact_sdk.add_group_welcome_template(**data)
        self.assertTrue('template_id' in return_data)
        # 删除群欢迎语素材
        self.assertEqual(self.external_contact_sdk.del_group_welcome_template(**return_data), {})

    def test_edit_group_welcome_template(self):
        """
        实现编辑群欢迎语素材的测试
        :return:
        """
        data = {
            "template_id": "msg6aZhCgAATofNkemU2lWczog6fyfwSg",
            "text": {"content": "您好，这里是量潮，很高兴为您服务！"}
        }
        return_data = self.external_contact_sdk.edit_group_welcome_template(**data)
        self.assertEqual(return_data, {})

    def test_edit_group_welcome_template_invalid_template_id(self):
        """
        实现编辑群欢迎语素材的测试：template_id错误
        :return:
        WeChatWorkSDK Error 40037: invalid template_id
        """
        data = {
            "template_id": "msgXXXXXXX",
            "text": {"content": "您好，这里是量潮，很高兴为您服务！"}
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.edit_group_welcome_template, **data)

    def test_get_group_welcome_template(self):
        """
        实现获取群欢迎语素材的测试
        :return:
        """
        data = {"template_id": "msg6aZhCgAATofNkemU2lWczog6fyfwSg"}
        return_data = self.external_contact_sdk.get_group_welcome_template(**data)
        self.assertTrue('text' in return_data)

    def test_get_group_welcome_template_invalid_template_id(self):
        """
        实现获取群欢迎语素材的测试：template_id错误
        :return:
        WeChatWorkSDK Error 40037: invalid template_id
        """
        data = {"template_id": "msgXXXXXXX"}
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_group_welcome_template, **data)

    def test_del_group_welcome_template_invalid_template_id(self):
        """
        实现删除群欢迎语素材的测试：template_id错误
        :return:
        WeChatWorkSDK Error 40037: invalid template_id
        """
        data = {"template_id": "msgXXXXXXX"}
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.del_group_welcome_template, **data)

    def test_get_unassigned_list(self):
        """
        实现获取离职成员的客户列表的测试
        :return:
        """
        data = {'page_id': 0, "page_size": 10}
        return_data = self.external_contact_sdk.get_unassigned_list(**data)
        self.assertTrue('info' in return_data)

    def test_external_contact_transfer_not_external_contact(self):
        """
        实现离职成员的外部联系人再分配的测试：不存在外部联系人的关系，即指定的外部联系人userid不存在
        :return:
        WeChatWorkSDK Error 84061: not external contact
        """
        data = {
            "external_userid": "wm6aZhCgAAKnotxPtAz68KmVbNubRr6g",
            "handover_userid": "HeLiJian",
            "takeover_userid": "ChenFangZhou"
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.external_contact_transfer, **data)

    def test_external_contact_transfer_invalid_userid(self):
        """
        实现离职成员的外部联系人再分配的测试：handover_userid错误
        :return:
        WeChatWorkSDK Error 40003: invalid userid
        """
        data = {
            "external_userid": "wm6aZhCgAAKnotxPtAz68KmVbNubRr6g",
            "handover_userid": "MaYongKang",
            "takeover_userid": "ChenFangZhou"
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.external_contact_transfer, **data)

    def test_external_contact_transfer_user_not_resigned_from_corp(self):
        """
        实现离职成员的外部联系人再分配的测试：该成员尚未离职，handover_userid需更换
        :return:
        WeChatWorkSDK Error 40097: user not resigned from corp
        """
        data = {
            "external_userid": "wm6aZhCgAAzqC7KP5-oPV4UvpJmHhOcA",
            "handover_userid": "ChenFan",
            "takeover_userid": "ChenFangZhou"
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.external_contact_transfer, **data)

    def test_groupchat_transfer_group_is_already_inherited(self):
        """
        实现离职成员的群再分配的测试：离职群已经继承
        :return:
        """
        data = {
            "chat_id_list": ["wr6aZhCgAAqh24yCnF3W0oO66mFZGRKA"],
            "new_owner": "ChenFan"
        }
        return_data = self.external_contact_sdk.groupchat_transfer(**data)
        self.assertTrue('failed_chat_list' in return_data)
        self.assertEqual(return_data['failed_chat_list'][0]['errcode'], 90508)

    def test_groupchat_transfer_owner_not_resigned_from_corp(self):
        """
        实现离职成员的群再分配的测试：群主未离职
        :return:
        """
        data = {
            "chat_id_list": ["wr6aZhCgAA1g9wJtYmMT6RDW6L5aQc4A"],
            "new_owner": "ChenFan"
        }
        return_data = self.external_contact_sdk.groupchat_transfer(**data)
        self.assertTrue('failed_chat_list' in return_data)
        self.assertEqual(return_data['failed_chat_list'][0]['errcode'], 90500)

    def test_get_transfer_result(self):
        """
        实现查询客户接替结果的测试
        :return:
        """
        data = {
            "external_userid": "wm6aZhCgAAKnotxPtAz68KmVbNubRr6g",
            "handover_userid": "HeLiJian",
            "takeover_userid": "ChenFangZhou"
        }
        return_data = self.external_contact_sdk.get_transfer_result(**data)
        self.assertEqual(return_data['status'], 1)
        self.assertTrue('takeover_time' in return_data)

    def test_get_transfer_result_no_takeover_record(self):
        """
        实现查询客户接替结果的测试：无接替记录
        :return:
        """
        data = {
            "external_userid": "wm6aZhCgAAz30AL_aEd-GdEtEcqb7iXw",
            "handover_userid": "HeLiJian",
            "takeover_userid": "ChenFan"
        }
        return_data = self.external_contact_sdk.get_transfer_result(**data)
        self.assertEqual(return_data['status'], 5)
        self.assertFalse('takeover_time' in return_data)

    def test_get_user_behavior_data(self):
        """
        实现获取联系客户统计数据的测试
        :return:
        """
        # 2020-07-20到2020-08-02的数据
        data = {
            "userid": ['ChenFangZhou', 'ChenFan'],
            "partyid": [1],
            "start_time": 1595174400,
            "end_time": 1596297600
        }
        return_data = self.external_contact_sdk.get_user_behavior_data(**data)
        self.assertTrue('behavior_data' in return_data)

    def test_get_user_behavior_data_invalid_start_end_time(self):
        """
        实现获取联系客户统计数据的测试：无效的起始结束时间。此处为无效的起始时间。
        :return:
        WeChatWorkSDK Error 600018: invalid start endtime
        """
        data = {
            "userid": ['ChenFangZhou', 'ChenFan'],
            "partyid": [1],
            "start_time": 1095174400,
            "end_time": 1596297600
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_user_behavior_data, **data)

    def test_get_user_behavior_data_invalid_partyid(self):
        """
        实现获取联系客户统计数据的测试：无效的部门id
        :return:
        WeChatWorkSDK Error 60123: invalid party id
        """
        data = {
            "userid": ['ChenFangZhou', 'ChenFan'],
            "partyid": [7],
            "start_time": 1595174400,
            "end_time": 1596297600
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_user_behavior_data, **data)

    def test_get_groupchat_data(self):
        """
        实现获取客户群统计数据的测试
        :return:
        """
        data = {
            "day_begin_time": 1595174400,
            "owner_filter": {},
            "order_by": 2,
            "order_asc": 0,
            "offset": 0,
            "limit": 100
        }
        return_data = self.external_contact_sdk.get_groupchat_data(**data)
        self.assertTrue('items' in return_data)

    def test_get_groupchat_data_invalid_start_time(self):
        """
        实现获取客户群统计数据的测试： 无效的起始时间
        :return:
        WeChatWorkSDK Error 600018: invalid start time
        """
        data = {
            "day_begin_time": 1095174400,
            "owner_filter": {},
            "order_by": 2,
            "order_asc": 0,
            "offset": 0,
            "limit": 100
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_groupchat_data, **data)

    def test_get_groupchat_data_invalid_partyid(self):
        """
        实现获取客户群统计数据的测试： 无效的部门id
        :return:
        WeChatWorkSDK Error 60123: invalid party id
        """
        data = {
            "day_begin_time": 1595174400,
            "owner_filter": {"partyid_list": [7]},
            "order_by": 2,
            "order_asc": 0,
            "offset": 0,
            "limit": 100
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_groupchat_data, **data)

    def test_get_groupchat_data_invalid_argument_order_by(self):
        """
        实现获取客户群统计数据的测试： 不合法的参数。order_by只能取1、2、3、4
        :return:
        WeChatWorkSDK Error 40058: order_by invalid
        """
        data = {
            "day_begin_time": 1595174400,
            "owner_filter": {},
            "order_by": 0,
            "order_asc": 2,
            "offset": 0,
            "limit": 100
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_groupchat_data, **data)

    def test_get_groupchat_data_invalid_argument_order_asc(self):
        """
        实现获取客户群统计数据的测试：不合法的参数。order_asc只能取0、1
        :return:
        WeChatWorkSDK Error 40058: order_asc invalid
        """
        data = {
            "day_begin_time": 1595174400,
            "owner_filter": {},
            "order_by": 2,
            "order_asc": 2,
            "offset": 0,
            "limit": 100
        }
        self.assertRaises(WeChatWorkSDKException, self.external_contact_sdk.get_groupchat_data, **data)


if __name__ == '__main__':
    unittest.main()
