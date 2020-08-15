# -*- coding: utf-8 -*-

import time
from .base import WeChatWorkSDK


class ExternalContactSDK(WeChatWorkSDK):
    API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'externalcontact/'

    def get_follow_user_list(self):
        """
        获取配置了客户联系功能的成员列表
        :return: follow_user: 配置了客户联系功能的成员userid列表
        """
        return self.get_api(api='get_follow_user_list', query_params=None)

    def get_external_contact_list(self, userid: str):
        """
        获取客户列表: 企业可通过此接口获取指定成员添加的客户列表。客户是指配置了客户联系功能的成员所添加的外部联系人。
        没有配置客户联系功能的成员，所添加的外部联系人将不会作为客户返回。
        :param userid: 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。
        :return: external_userid: 外部联系人的userid列表。
        """
        return self.get_api(api='list', query_params={'userid': userid})

    def get_external_contact_details(self, external_userid: str):
        """
        获取客户详情: 企业可通过此接口，根据外部联系人的userid，获取客户详情。
        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号。必须填写。
        :return: external_contact: 客户详情，主要包括
                 external_userid: 外部联系人的userid
                 name: 外部联系人的名称。如果外部联系人为微信用户，则返回外部联系人的名称为其微信昵称；
                 如果外部联系人为企业微信用户，则会按照以下优先级顺序返回：
                 此外部联系人或管理员设置的昵称、认证的实名和账号名称
                 type: 外部联系人的类型，1表示该外部联系人是微信用户，2表示该外部联系人是企业微信用户
                 gender: 外部联系人性别 0-未知 1-男性 2-女性
                 # 以下字段仅当联系人类型是企业微信用户时才有
                 position: 外部联系人的职位，如果外部企业或用户选择隐藏职位，则不返回
                 corp_name: 外部联系人所在企业的简称
                 corp_full_name: 外部联系人所在企业的主体名称
                 external_profile: 外部联系人的自定义展示信息，可以有多个字段和多种类型，包括文本，网页和小程序
        """
        return self.get_api(api='get', query_params={'external_userid': external_userid})

    def edit_external_contact_remark(self, userid: str, external_userid: str, remark: str = "",
                                     description: str = "", remark_company: str = "", remark_mobiles=""):
        """
        修改客户备注信息: 企业可通过此接口修改指定用户添加的客户的备注信息
        :param userid: 企业成员的userid。必须填写
        :param external_userid: 外部联系人userid。必须填写
        :param remark: 此用户对外部联系人的备注，最多20个字符
        :param description: 此用户对外部联系人的描述，最多150个字符
        :param remark_company: 此用户对外部联系人备注的所属公司名称，最多20个字符。只在此外部联系人为微信用户时有效。
        :param remark_mobiles: 此用户对外部联系人备注的手机号
        data = {
            "userid":"zhangsan",
            "external_userid":"woAJ2GCAAAd1asdasdjO4wKmE8Aabj9AAA",
            "remark":"备注信息",
            "description":"描述信息",
            "remark_company":"腾讯科技",
            "remark_mobiles":["13800000001", "13800000002"],
        }
        remark，description，remark_company，remark_mobiles不可同时为空。
        如果填写了remark_mobiles，将会覆盖旧的备注手机号。
        :return: {}
        """
        data = {
            "user_id": userid,
            "external_userid": external_userid,
            "remark": remark,
            "description": description,
            "remark_company": remark_company,
            "remark_mobiles": remark_mobiles
        }
        return self.post_api(api='remark', query_params=None, data=data)

    def get_corp_tag_list(self, tag_id=None):
        """
        获取企业标签库: 企业可通过此接口获取企业客户标签详情
        :param tag_id: 要查询的标签id，如果不填则获取该企业的所有客户标签，目前暂不支持标签组id
        # 一般：tag_id="et6aZhCgAAH_bZ-L3Q6Hn5cq-Y1jquRg"
        # 重要：tag_id="et6aZhCgAAfudx66ooq6o373_XVmx_Rw"
        # 核心：tag_id="et6aZhCgAAwVDwwsZSc4WEs3HH7wvaVw"
        :return: tag_group: 标签组列表
        tag_group.group_id: 标签组id
        tag_group.group_name: 标签组名称
        tag_group.create_time: 标签组创建时间
        tag_group.order: 标签组排序的次序值，order值大的排序靠前。有效的值范围是[0, 2^32)
        tag_group.deleted: 标签组是否已经被删除，只在指定tag_id进行查询时返回
        tag_group.tag: 标签组内的标签列表
        tag_group.tag.id: 标签id
        tag_group.tag.name: 标签名称
        tag_group.tag.create_time: 标签创建时间
        tag_group.tag.order: 标签排序的次序值，order值大的排序靠前。有效的值范围是[0, 2^32)
        tag_group.tag.deleted: 标签是否已经被删除，只在指定tag_id进行查询时返回
        """
        if tag_id is None:
            tag_id = []
        return self.post_api(api='get_corp_tag_list', query_params=None, data={'tag_id': tag_id})

    def add_corp_tag(self, tag, group_id=None, group_name=None, order=None):
        """
        添加企业客户标签: 企业可通过此接口向客户标签库中添加新的标签组和标签
        :param group_id: 标签组id
        :param group_name: 标签组名称，最长为30个字符
        :param order: 标签组次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        :param tag: [{"name": "TAG_NAME_1", "order": 1}]
               tag.name: 添加的标签名称，最长为30个字符，必须填写
               tag.order: 标签次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        data = {
            "group_id": "GROUP_ID",
            "group_name": "GROUP_NAME",
            "order": 1,
            "tag": [{"name": "TAG_NAME_1", "order": 1},
                    {"name": "TAG_NAME_2", "order": 2}]
        }
        注:
        1. 如果要向指定的标签组下添加标签，需要填写group_id参数
        2. 如果要创建一个全新的标签组以及标签，则需要通过group_name参数指定新标签组名称
        3. 如果填写的group_name已经存在，则会在此标签组下新建标签
        4. 如果填写了group_id参数，则group_name和标签组的order参数会被忽略
        5. 不支持创建空标签组
        6. 标签组内的标签不可同名，如果传入多个同名标签，则只会创建一个
        :return: tag_group: 标签组列表
        """
        if group_id is None:
            group_id = ""
        if group_name is None:
            group_name = ""
        if order is None:
            data = {
                "group_id": group_id,
                "group_name": group_name,
                "tag": tag
            }
        else:
            data = {
                "group_id": group_id,
                "group_name": group_name,
                "order": order,
                "tag": tag
            }
        return self.post_api(api='add_corp_tag', query_params=None, data=data)

    def edit_corp_tag(self, tag_id: str, new_tag_name: str, order=None):
        """
        编辑企业客户标签: 企业可通过此接口编辑客户标签/标签组的名称或次序值
        :param tag_id: 标签或标签组的id列表，必须填写
        :param new_tag_name: 新的标签或标签组名称，最长为30个字符
        :param order: 标签/标签组的次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        data = {"id": "TAG_ID", "name": "NEW_TAG_NAME", "order": 1}
        :return: {}
        """
        if order is None:
            data = {"id": tag_id, "name": new_tag_name}
        else:
            data = {"id": tag_id, "name": new_tag_name, "order": order}
        return self.post_api(api='edit_corp_tag', query_params=None, data=data)

    def del_corp_tag(self, tag_id, group_id):
        """
        删除企业客户标签: 企业可通过此接口删除客户标签库中的标签，或删除整个标签组
        :param tag_id: 标签的id列表
        :param group_id: 标签组的id列表
        data = {"tag_id": ["TAG_ID_1", "TAG_ID_2"], "group_id": ["GROUP_ID_1", "GROUP_ID_2"]}
        :return: {}
        """
        data = {"tag_id": tag_id, "group_id": group_id}
        return self.post_api(api='del_corp_tag', query_params=None, data=data)

    def edit_external_contact_corp_tag(self, userid: str, external_userid: str, add_tag=None, remove_tag=None):
        """
        编辑客户企业标签: 企业可通过此接口为指定成员的客户添加上由企业统一配置的标签
        :param userid: 添加外部联系人的userid。必须填写
        :param external_userid: 外部联系人userid。请确保external_userid是userid的外部联系人。必须填写
        :param add_tag: 要标记的标签列表，列表中元素为tag_id
        :param remove_tag: 要移除的标签列表，列表中元素为tag_id
        add_tag和remove_tag不可同时为空。
        :return: {}
        """
        if add_tag is None:
            add_tag = []
        if remove_tag is None:
            remove_tag = []
        data = {
            "userid": userid,
            "external_userid": external_userid,
            "add_tag": add_tag,
            "remove_tag": remove_tag
        }
        return self.post_api(api='mark_tag', query_params=None, data=data)

    def get_groupchat_list(self, status_filter: int, limit: int, offset: int = 0,
                           userid_list=None, partyid_list=None):
        """
        获取客户群列表: 该接口用于获取配置过客户群管理的客户群列表
        :param status_filter: 群状态过滤。0表示所有列表，1表示离职待继承，2表示离职继承中，3表示离职继承完成。默认为0
        :param offset: 分页，偏移量。默认为0
        :param limit: 分页，预期请求的数据量，取值范围1~1000。必须填写
        offset + limit总数不能大于5万。数据量太多的话，需要用参数 owner_filter 来过滤
        :param userid_list: 用户ID列表。最多100个
        :param partyid_list: 部门ID列表。最多100个
        :return:
        group_chat_list: 客户群列表
        chat_id: 客户群ID
        status: 客户群状态。0表示正常，1表示跟进人离职，2表示离职继承中，3表示离职继承完成
        """
        if userid_list is None:
            userid_list = []
        if partyid_list is None:
            partyid_list = []
        data = {
            "status_filter": status_filter,
            "owner_filter": {
                "userid_list": userid_list,
                "partyid_list": partyid_list
            },
            "offset": offset,
            "limit": limit
        }
        return self.post_api(api='groupchat/list', query_params=None, data=data)

    def get_groupchat_details(self, chat_id: str):
        """
        获取客户群详情: 通过客户群ID，获取详情。包括群名、群成员列表、群成员入群时间、入群方式。
        说明: 客户群是由具有客户群使用权限的成员创建的外部群
        :param chat_id: 客户群ID
        :return: group_chat: 客户群详情，主要包括
                 chat_id: 客户群ID
                 name: 群名
                 owner: 群主ID
                 create_time: 群的创建时间
                 notice: 群公告
                 member_list: 群成员列表
                 userid: 群成员id
                 type: 成员类型。1表示企业成员，2表示外部联系人
                 join_time: 入群时间
                 join_scene: 入群方式。1表示由成员邀请入群（直接邀请入群），
                 2表示由成员邀请入群（通过邀请链接入群），3表示通过扫描群二维码入群
        """
        data = {'chat_id': chat_id}
        return self.post_api(api='groupchat/get', query_params=None, data=data)

    def add_msg_template(self, ):
        pass

    def get_unassigned_list(self, page_id: int = 0, page_size: int = 1000):
        """
        获取离职成员的客户列表: 企业和第三方可通过此接口，获取所有离职成员的客户列表，
        并可进一步调用离职成员的外部联系人再分配接口将这些客户重新分配给其他企业成员。
        :param page_id: 分页查询，要查询页号，从0开始
        :param page_size: 每次返回的最大记录数，默认为1000，最大值为1000
        :return: 返回数据按离职时间的降序排列，当page_id为1，page_size为100时，表示取第101到第200条记录
        info.handover_userid: 离职成员的userid
        info.external_userid: 外部联系人userid
        info.dimission_time: 成员离职时间
        is_last: 是否是最后一条记录
        """
        data = {'page_id': page_id, "page_size": page_size}
        return self.post_api(api='get_unassigned_list', query_params=None, data=data)

    def external_contact_transfer(self, external_userid: str, handover_userid: str, takeover_userid: str):
        """
        离职成员的外部联系人再分配: 企业可通过此接口，将已离职成员的外部联系人分配给另一个成员接替联系
        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号
        必须是handover_userid的客户（即配置了客户联系功能的成员所添加的联系人）
        :param handover_userid: 离职成员的userid
        :param takeover_userid: 接替成员的userid
        :return: {}
        """
        data = {
            'external_userid': external_userid,
            'handover_userid': handover_userid,
            'takeover_userid': takeover_userid
        }
        return self.post_api(api='transfer', query_params=None, data=data)

    def groupchat_transfer(self, chat_id_list, new_owner: str):
        """
        离职成员的群再分配: 企业可通过此接口，将已离职成员为群主的群，分配给另一个客服成员
        :param chat_id_list: 需要转群主的客户群ID列表。取值范围：1 ~ 100
        :param new_owner: 新群主ID
        注:
        1. 群主离职了的客户群，才可继承
        2. 继承给的新群主，必须是配置了客户联系功能的成员
        3. 继承给的新群主，必须有设置实名
        4. 继承给的新群主，必须有激活企业微信
        5. 同一个人的群，限制每天最多分配300个给新群主
        :return: failed_chat_list: 没能成功继承的群
        failed_chat_list.chat_id: 没能成功继承的群ID
        failed_chat_list.errcode: 没能成功继承的群，错误码
        failed_chat_list.errmsg: 没能成功继承的群，错误描述
        """
        data = {"chat_id_list": chat_id_list, "new_owner": new_owner}
        return self.post_api(api='groupchat/transfer', query_params=None, data=data)

    def get_user_behavior_data(self, userid, partyid, start_time: str, end_time: str):
        """
        获取联系客户统计数据: 企业可通过此接口获取成员联系客户的数据，
        包括发起申请数、新增客户数、聊天数、发送消息数和删除/拉黑成员的客户数等指标
        :param userid: 成员ID列表。userid和partyid不可同时为空
        :param partyid: 部门ID列表。userid和partyid不可同时为空
        :param start_time: 数据起始时间，如2020-08-01。必须填写
        :param end_time: 数据结束时间，如2020-08-02。必须填写
        :return:
        behavior_data.stat_time: 数据日期，为当日0点的时间戳
        behavior_data.new_apply_cnt: 发起申请数，成员通过「搜索手机号」、「扫一扫」、
        「从微信好友中添加」、「从群聊中添加」、「添加共享、分配给我的客户」、
        「添加单向、双向删除好友关系的好友」、「从新的联系人推荐中添加」等渠道主动向客户发起的好友申请数量。
        behavior_data.new_contact_cnt: 新增客户数，成员新添加的客户数量。
        behavior_data.chat_cnt: 聊天总数， 成员有主动发送过消息的单聊总数。
        behavior_data.message_cnt: 发送消息数，成员在单聊中发送的消息总数。
        behavior_data.reply_percentage: 已回复聊天占比，客户主动发起聊天后，
        成员在一个自然日内有回复过消息的聊天数/客户主动发起的聊天数比例，不包括群聊，仅在确有回复时返回。
        behavior_data.avg_reply_time: 平均首次回复时长，单位为分钟，
        即客户主动发起聊天后，成员在一个自然日内首次回复的时长间隔为首次回复时长，
        所有聊天的首次回复总时长/已回复的聊天总数即为平均首次回复时长，不包括群聊，仅在确有回复时返回。
        behavior_data.negative_feedback_cnt: 删除/拉黑成员的客户数，即将成员删除或加入黑名单的客户数。
        """
        start_time_timestamp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d")))
        end_time_timestamp = int(time.mktime(time.strptime(end_time, "%Y-%m-%d")))
        data = {
            "userid": userid,
            "partyid": partyid,
            "start_time": start_time_timestamp,
            "end_time": end_time_timestamp
        }
        return self.post_api(api='get_user_behavior_data', query_params=None, data=data)

    def get_groupchat_data(self, day_begin_time: str, userid_list=None, partyid_list=None,
                           order_by: int = 1, order_asc: int = 0, offset: int = 0, limit: int = 500):
        """
        获取客户群统计数据: 获取指定日期全天的统计数据。注意，企业微信仅存储180天的数据。
        :param day_begin_time: 开始时间，填当天开始的0分0秒（否则系统自动处理为当天的0分0秒）。
        取值范围：昨天至前180天。必须填写
        owner_filter: 群主过滤，如果不填，表示获取全部群主的数据
        :param userid_list: 群主ID列表。最多100个
        :param partyid_list: 群主所属部门ID列表。最多100个
        :param order_by: 排序方式。1表示新增群的数量，2表示群总数，3表示新增群人数，4表示群总人数。默认为1
        :param order_asc: 是否升序。0表示否；1表示是。默认降序
        :param offset: 分页，偏移量，默认为0
        :param limit: 分页，预期请求的数据量，默认为500，取值范围为1 ~ 1000
        :return:
        total: 命中过滤条件的记录总个数
        next_offset: 当前分页的下一个offset。当next_offset和total相等时，说明已经取完所有
        items: 记录列表。表示某个群主所拥有的客户群的统计数据
        owner: 群主ID
        data: 详情
        new_chat_cnt: 新增客户群数量
        chat_total: 截至当天客户群总数量
        chat_has_msg: 截至当天有发过消息的客户群数量
        new_member_cnt: 客户群新增群人数
        member_total: 截至当天客户群总人数
        member_has_msg: 截至当天有发过消息的群成员数
        msg_total: 截至当天客户群消息总数
        """
        if userid_list is None:
            userid_list = []
        if partyid_list is None:
            partyid_list = []
        day_begin_time_stamp = int(time.mktime(time.strptime(day_begin_time, "%Y-%m-%d")))
        data = {
            "day_begin_time": day_begin_time_stamp,
            "owner_filter": {
                "userid_list": userid_list,
                "partyid_list": partyid_list
            },
            "order_by": order_by,
            "order_asc": order_asc,
            "offset": offset,
            "limit": limit
        }
        return self.post_api(api='groupchat/statistic', query_params=None, data=data)

