# -*- coding: utf-8 -*-

from wechatwork_sdk.base import WeChatWorkSDK
from wechatwork_sdk.exception import WeChatWorkSDKException


class ExternalContactSDK(WeChatWorkSDK):
    def __init__(self, corpid, secret):
        super().__init__(corpid, secret)
        self._api_root_url = self._api_root_url + 'externalcontact/'

    def get_follow_user_list(self) -> dict:
        """
        获取配置了客户联系功能的成员列表
        :return: dict，包括以下字段
            - follow_user: 配置了客户联系功能的成员userid列表
        """
        try:
            return self.get_api(api='get_follow_user_list', query_params=None)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_external_contact_list(self, userid: str) -> dict:
        """
        获取客户列表: 企业可通过此接口获取指定成员添加的客户列表。客户是指配置了客户联系功能的成员所添加的外部联系人。
        没有配置客户联系功能的成员，所添加的外部联系人将不会作为客户返回。
        :param userid: 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。
        :return: dict，包括以下字段
            - external_userid: 外部联系人的userid列表。
        错误码84061表示不存在外部联系人的关系，即该成员没有客户联系功能
        """
        try:
            return self.get_api(api='list', query_params={'userid': userid})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_external_contact_details(self, external_userid: str) -> dict:
        """
        获取客户详情: 企业可通过此接口，根据外部联系人的userid，获取客户详情。
        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号。必须填写。
        :return: dict，包括以下字段
            - external_contact: 客户详情: dict，包括以下字段
                - external_userid: 外部联系人的userid
                - name: 外部联系人的名称。如果外部联系人为微信用户，则返回外部联系人的名称为其微信昵称；
                        如果外部联系人为企业微信用户，则会按照以下优先级顺序返回：
                        此外部联系人或管理员设置的昵称、认证的实名和账号名称
                - type: 外部联系人的类型，1-该外部联系人是微信用户，2-该外部联系人是企业微信用户
                - gender: 外部联系人性别，0-未知 1-男性 2-女性
                # 以下字段仅当联系人类型是企业微信用户时才有
                - position: 外部联系人的职位，如果外部企业或用户选择隐藏职位，则不返回
                - corp_name: 外部联系人所在企业的简称
                - corp_full_name: 外部联系人所在企业的主体名称
                - external_profile: 外部联系人的自定义展示信息，可以有多个字段和多种类型，包括文本，网页和小程序
        错误码40096表示不合法的外部联系人userid，即指定的外部联系人userid不存在
        错误码41035表示缺少外部联系人userid参数，即external_userid为空或未填写
        """
        try:
            return self.get_api(api='get', query_params={'external_userid': external_userid})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def edit_external_contact_remark(self, **info) -> dict:
        """
        修改客户备注信息: 企业可通过此接口修改指定用户添加的客户的备注信息
        :param info: 客户备注信息: dict，包括以下字段
            - userid: 企业成员的userid。必须填写
            - external_userid: 外部联系人userid。必须填写
            - remark: 此用户对外部联系人的备注，最多20个字符
            - description: 此用户对外部联系人的描述，最多150个字符
            - remark_company: 此用户对外部联系人备注的所属公司名称，最多20个字符。只在此外部联系人为微信用户时有效。
            - remark_mobiles: 此用户对外部联系人备注的手机号
            - remark_pic_mediaid: 备注图片的mediaid
        注：
        1. remark，description，remark_company，remark_mobiles，remark_pic_mediaid不可同时为空
        2. 如果填写了remark_mobiles，将会覆盖旧的备注手机号
        示例：
        info = {
            "userid":"zhangsan",
            "external_userid":"woAJ2GCAAAd1asdasdjO4wKmE8Aabj9AAA",
            "remark":"备注信息",
            "description":"描述信息",
            "remark_company":"腾讯科技",
            "remark_mobiles":["13800000001", "13800000002"],
            "remark_pic_mediaid":"MEDIAID"
        }
        :return: {}
        错误码40096表示不合法的外部联系人userid，即指定的外部联系人userid不存在
        错误码84061表示不存在外部联系人的关系，即该成员没有客户联系功能
        """
        try:
            return self.post_api(api='remark', query_params=None, data=info)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_corp_tag_list(self, tag_id=None) -> dict:
        """
        获取企业标签库: 企业可通过此接口获取企业客户标签详情
        :param tag_id: 要查询的标签id，如果不填则获取该企业的所有客户标签，目前暂不支持标签组id
        示例：
        一般：tag_id="et6aZhCgAAH_bZ-L3Q6Hn5cq-Y1jquRg"
        重要：tag_id="et6aZhCgAAfudx66ooq6o373_XVmx_Rw"
        核心：tag_id="et6aZhCgAAwVDwwsZSc4WEs3HH7wvaVw"
        :return: dict，包括以下字段
            - tag_group: 标签组列表，包括
                - tag_group.group_id: 标签组id
                - tag_group.group_name: 标签组名称
                - tag_group.create_time: 标签组创建时间
                - tag_group.order: 标签组排序的次序值，order值大的排序靠前。有效的值范围是[0, 2^32)
                - tag_group.deleted: 标签组是否已经被删除，只在指定tag_id进行查询时返回
                - tag_group.tag: 标签组内的标签列表，包括若干个dict，其中字段包括
                    - tag_group.tag.id: 标签id
                    - tag_group.tag.name: 标签名称
                    - tag_group.tag.create_time: 标签创建时间
                    - tag_group.tag.order: 标签排序的次序值，order值大的排序靠前。有效的值范围是[0, 2^32)
                    - tag_group.tag.deleted: 标签是否已经被删除，只在指定tag_id进行查询时返回
        错误码40068表示不合法的标签ID，即标签ID未指定，或者指定的标签ID不存在
        """
        try:
            if tag_id is None:
                tag_id = []
            return self.post_api(api='get_corp_tag_list', query_params=None, data={'tag_id': tag_id})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def add_corp_tag(self, **data) -> dict:
        """
        添加企业客户标签: 企业可通过此接口向客户标签库中添加新的标签组和标签
        :param data: dict，包括以下字段
            - group_id: 标签组id
            - group_name: 标签组名称，最长为30个字符
            - order: 标签组次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
            - tag: 标签列表，包括若干个dict，其中字段包括
                - tag.name: 添加的标签名称，最长为30个字符，必须填写
                - tag.order: 标签次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        示例：
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
        :return: dict，包括以下字段
            - tag_group: 标签组: dict，包括以下字段
                - tag_group.group_id: 标签组id
                - tag_group.group_name: 标签组名称
                - tag_group.create_time: 标签组创建时间
                - tag_group.order: 标签组次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
                - tag_group.tag: 标签组内的标签列表，包括若干个dict，其中字段包括
                    - tag_group.tag.id: 新建标签id
                    - tag_group.tag.name: 新建标签名称
                    - tag_group.tag.create_time: 标签创建时间
                    - tag_group.tag.order: 标签次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        错误码40071表示不合法的标签名字，即标签名字已经存在
        错误码40072表示不合法的标签名字长度，标签名不允许为空，最大长度限制为32个字（汉字或英文字母）
        错误码41018表示缺少tag.name
        """
        try:
            return self.post_api(api='add_corp_tag', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def edit_corp_tag(self, **tag) -> dict:
        """
        编辑企业客户标签: 企业可通过此接口编辑客户标签/标签组的名称或次序值
        :param tag: 企业客户标签信息: dict，包括以下字段
            - id: 标签或标签组的id列表，必须填写
            - new_tag_name: 新的标签或标签组名称，最长为30个字符
            - order: 标签/标签组的次序值。order值大的排序靠前。有效的值范围是[0, 2^32)
        示例：
        tag = {"id": "TAG_ID", "name": "NEW_TAG_NAME", "order": 1}
        :return: {}
        错误码40071表示不合法的标签名字，即标签名字已经存在
        错误码40072表示不合法的标签名字长度，标签名不允许为空，最大长度限制为32个字（汉字或英文字母）
        错误码41017表示缺少tag_id
        """
        try:
            return self.post_api(api='edit_corp_tag', query_params=None, data=tag)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def del_corp_tag(self, **tag) -> dict:
        """
        删除企业客户标签: 企业可通过此接口删除客户标签库中的标签，或删除整个标签组
        :param tag: dict，包括以下字段
            - tag_id: 标签的id列表
            - group_id: 标签组的id列表
        注：
        1. tag_id和group_id不可同时为空
        2. 如果一个标签组下所有的标签均被删除，则标签组会被自动删除
        示例：
        data = {"tag_id": ["TAG_ID_1", "TAG_ID_2"], "group_id": ["GROUP_ID_1", "GROUP_ID_2"]}
        :return: {}
        错误码40068表示不合法的标签ID，即标签ID未指定，或者指定的标签ID不存在
        错误码41017表示缺少tag_id参数
        """
        try:
            return self.post_api(api='del_corp_tag', query_params=None, data=tag)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def edit_external_contact_corp_tag(self, **tag) -> dict:
        """
        编辑客户企业标签: 企业可通过此接口为指定成员的客户添加上由企业统一配置的标签
        :param tag: dict，包括以下字段
            - userid: 添加外部联系人的userid。必须填写
            - external_userid: 外部联系人userid。请确保external_userid是userid的外部联系人。必须填写
            - add_tag: 要标记的标签列表，列表中元素为tag_id
            - remove_tag: 要移除的标签列表，列表中元素为tag_id
        注：add_tag和remove_tag不可同时为空。
        :return: {}
        错误码40068表示不合法的标签ID，即指定的标签ID不存在
        错误码41017表示缺少tag_id
        错误码84061表示不存在外部联系人的关系，即指定的外部联系人userid不存在
        """
        try:
            return self.post_api(api='mark_tag', query_params=None, data=tag)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_groupchat_list(self, **data) -> dict:
        """
        获取客户群列表: 该接口用于获取配置过客户群管理的客户群列表
        :param data: dict，包括以下字段
            - status_filter: 群状态过滤。0-所有列表，1-离职待继承，2-离职继承中，3-离职继承完成。默认为0
            - owner_filter: 群主过滤: dict。如果不填，表示获取全部群主的数据。包括以下字段
                - userid_list: 用户ID列表。最多100个
                - partyid_list: 部门ID列表。最多100个
            - offset: 分页，偏移量。默认为0
            - limit: 分页，预期请求的数据量，取值范围1~1000。必须填写
        注：offset + limit总数不能大于5万。数据量太多的话，需要用参数owner_filter来过滤
        :return: dict，包括以下字段
            - group_chat_list: 客户群列表，包括若干个dict，其中字段包括
                - chat_id: 客户群ID
                - status: 客户群状态。0-正常，1-跟进人离职，2-离职继承中，3-离职继承完成
        """
        try:
            return self.post_api(api='groupchat/list', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_groupchat_details(self, chat_id: str) -> dict:
        """
        获取客户群详情: 通过客户群ID，获取详情。包括群名、群成员列表、群成员入群时间、入群方式。
        说明: 客户群是由具有客户群使用权限的成员创建的外部群
        :param chat_id: 客户群ID
        :return: dict，包括以下字段
            - group_chat: 客户群详情: dict，包括以下字段
                - chat_id: 客户群ID
                - name: 群名
                - owner: 群主ID
                - create_time: 群的创建时间
                - notice: 群公告
                - member_list: 群成员列表，包括若干个dict，其中字段包括
                    - userid: 群成员id
                    - type: 成员类型。1表示企业成员，2表示外部联系人
                    - join_time: 入群时间
                    - join_scene: 入群方式。1表示由成员邀请入群（直接邀请入群），
                                  2表示由成员邀请入群（通过邀请链接入群），3表示通过扫描群二维码入群
        错误码40050表示chat_id不存在
        """
        try:
            return self.post_api(api='groupchat/get', query_params=None, data={'chat_id': chat_id})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def add_msg_template(self, **data) -> dict:
        """
        添加企业群发消息任务: 企业可通过此接口添加企业群发消息的任务并通知客服人员发送给相关客户或客户群
        :param data: dict，包括以下字段
            - chat_type: 群发任务的类型，默认为single，表示发送给客户，group表示发送给客户群
            - external_userid: 客户的外部联系人id列表，仅在chat_type为single时有效，
                               不可与sender同时为空，最多可传入1万个客户
            - sender: 发送企业群发消息的成员userid，当类型为发送给客户群时必填
            - text: dict，包括以下字段
                - text.content: 消息文本内容，最长为4000个字节
            - image: dict，包括以下字段
                - image.media_id: 图片的media_id，可以通过素材管理接口获得
                - image.pic_url: 图片的链接，仅可使用上传图片接口得到的链接
            - link: dict，包括以下字段
                - link.title: 图文消息标题
                - link.picurl: 图文消息封面的url
                - link.desc: 图文消息的描述，最长为512个字节
                - link.url: 图文消息的链接
            - miniprogram: dict，包括以下字段
                - miniprogram.title: 小程序消息标题，最长为64个字节
                - miniprogram.pic_media_id: 小程序消息封面的mediaid，封面图建议尺寸为520*416
                - miniprogram.appid: 小程序appid，必须是关联到企业的小程序应用
                - miniprogram.page: 小程序page路径
        注：
        1. 同一个企业每个自然月内仅可针对一个客户/客户群发送4条消息，超过限制的用户将会被忽略
        2. text、image、link和miniprogram四者不能同时为空
        3. text与另外三者可以同时发送，此时将会以两条消息的形式触达客户
        4. image、link和miniprogram只能有一个，如果三者同时填，则按image、link、miniprogram的优先顺序取参，
           也就是说，如果image与link同时传值，则只有image生效。
        5. image的media_id和pic_url只需填写一个，两者同时填写时使用media_id，二者不可同时为空
        6. 若有link字段，则title和url必须填写
        7. 若有miniprogram字段，则title、pic_media_id、appid、page必须填写
        :return: dict，包括以下字段
            - fail_list: 无效或无法发送的external_userid列表
            - msgid: 企业群发消息的id，可用于获取群发消息发送结果
        错误码40063表示缺少参数，如text、image、link和miniprogram四者不能同时为空
        错误码41048表示无可发送的客户，即该客户被发送的消息已超过限制
        """
        try:
            return self.post_api(api='add_msg_template', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_group_msg_result(self, msgid: str) -> dict:
        """
        获取企业群发消息发送结果: 企业可通过该接口获取到添加企业群发消息任务的群发发送结果
        :param msgid: 群发消息的id，通过添加企业群发消息模板接口返回
        :return: dict，包括以下字段
            - detail_list: 外部联系人列表: list，包括
                - detail_list.external_userid: 外部联系人userid
                - detail_list.chat_id: 外部客户群id
                - detail_list.userid: 企业服务人员的userid
                - detail_list.status: 发送状态。0-未发送，1-已发送，2-因客户不是好友导致发送失败，
                                      3-因客户已经收到其他群发消息导致发送失败
                - detail_list.send_time: 发送时间，发送状态为1时返回
        """
        try:
            return self.post_api(api='get_group_msg_result', query_params=None, data={'msgid': msgid})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def send_welcome_msg(self, **data) -> dict:
        """
        发送新客户欢迎语: 企业微信在向企业推送添加外部联系人事件时，会额外返回一个welcome_code，
        企业以此为凭据调用接口，即可通过成员向新添加的客户发送个性化的欢迎语
        :param data: dict，包括以下字段
            - welcome_code: 通过添加外部联系人事件推送给企业的发送欢迎语的凭证，有效期为20秒。必须填写
            - text: dict，包括以下字段
                - text.content: 消息文本内容，最长为4000个字节
            - image: dict，包括以下字段
                - image.media_id: 图片的media_id，可以通过素材管理接口获得
                - image.pic_url: 图片的链接，仅可使用上传图片接口得到的链接
            - link: dict，包括以下字段
                - link.title: 图文消息标题，最长为128字节
                - link.picurl: 图文消息封面的url
                - link.desc: 图文消息的描述，最长为512个字节
                - link.url: 图文消息的链接
            - miniprogram: dict，包括以下字段
                - miniprogram.title: 小程序消息标题，最长为64个字节
                - miniprogram.pic_media_id: 小程序消息封面的mediaid，封面图建议尺寸为520*416
                - miniprogram.appid: 小程序appid，必须是关联到企业的小程序应用
                - miniprogram.page: 小程序page路径
        注：
        1. text、image、link和miniprogram四者不能同时为空
        2. text与另外三者可以同时发送，此时将会以两条消息的形式触达客户
        3. image、link和miniprogram只能有一个，如果三者同时填，则按image、link、miniprogram的优先顺序取参，
           也就是说，如果image与link同时传值，则只有image生效。
        4. image的media_id和pic_url只需填写一个，两者同时填写时使用media_id，二者不可同时为空
        5. 若有link字段，则title和url必须填写
        6. 若有miniprogram字段，则title、pic_media_id、appid、page必须填写
        :return: {}
        """
        try:
            return self.post_api(api='send_welcome_msg', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def add_group_welcome_template(self, **data) -> dict:
        """
        添加群欢迎语素材: 企业可通过此API向企业的群欢迎语素材库中添加素材
        :param data: dict，包括以下字段
            - text: dict，包括以下字段
                - text.content: 消息文本内容，最长为3000个字节
            - image: dict，包括以下字段
                - image.media_id: 图片的media_id，可以通过素材管理接口获得
                - image.pic_url: 图片的链接，仅可使用上传图片接口得到的链接
            - link: dict，包括以下字段
                - link.title: 图文消息标题，最长为128字节
                - link.picurl: 图文消息封面的url
                - link.desc: 图文消息的描述，最长为512个字节
                - link.url: 图文消息的链接
            - miniprogram: dict，包括以下字段
                - miniprogram.title: 小程序消息标题，最长为64个字节
                - miniprogram.pic_media_id: 小程序消息封面的mediaid，封面图建议尺寸为520*416
                - miniprogram.appid: 小程序appid，必须是关联到企业的小程序应用
                - miniprogram.page: 小程序page路径
        注：
        1. text中支持配置多个%NICKNAME%(大小写敏感)形式的欢迎语，
           当配置了欢迎语占位符后，发送给客户时会自动替换为客户的昵称
        2. text、image、link和miniprogram四者不能同时为空
        3. text与另外三者可以同时发送，此时将会以两条消息的形式触达客户
        4. image、link和miniprogram只能有一个，如果三者同时填，则按image、link、miniprogram的优先顺序取参，
           也就是说，如果image与link同时传值，则只有image生效。
        5. image的media_id和pic_url只需填写一个，两者同时填写时使用media_id，二者不可同时为空
        6. 若有link字段，则title和url必须填写
        7. 若有miniprogram字段，则title、pic_media_id、appid、page必须填写
        :return: dict，板块以下字段
            - template_id: 欢迎语素材id
        """
        try:
            return self.post_api(api='group_welcome_template/add', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def edit_group_welcome_template(self, **data) -> dict:
        """
        编辑群欢迎语素材: 企业可通过此API编辑欢迎语素材库中的素材
        :param data: dict，包括以下字段
            - template_id: 欢迎语素材id。必须填写
            - text: dict，包括以下字段
                - text.content: 消息文本内容，最长为4000个字节
            - image: dict，包括以下字段
                - image.media_id: 图片的media_id，可以通过素材管理接口获得
                - image.pic_url: 图片的链接，仅可使用上传图片接口得到的链接
            - link: dict，包括以下字段
                - link.title: 图文消息标题，最长为128字节
                - link.picurl: 图文消息封面的url
                - link.desc: 图文消息的描述，最长为512个字节
                - link.url: 图文消息的链接
            - miniprogram: dict，包括以下字段
                - miniprogram.title: 小程序消息标题，最长为64个字节
                - miniprogram.pic_media_id: 小程序消息封面的mediaid，封面图建议尺寸为520*416
                - miniprogram.appid: 小程序appid，必须是关联到企业的小程序应用
                - miniprogram.page: 小程序page路径
        注：
        1. image、link和miniprogram只能有一个，如果三者同时填，则按image、link、miniprogram的优先顺序取参，
           也就是说，如果image与link同时传值，则只有image生效。
        2. image的media_id和pic_url只需填写一个，两者同时填写时使用media_id，二者不可同时为空
        3. 若有link字段，则title和url必须填写
        4. 若有miniprogram字段，则title、pic_media_id、appid、page必须填写
        :return: {}
        """
        try:
            return self.post_api(api='group_welcome_template/edit', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_group_welcome_template(self, template_id: str) -> dict:
        """
        获取群欢迎语素材: 企业可通过此API获取群欢迎语素材
        :param template_id: 群欢迎语的素材id
        :return: dict，包括以下字段（image、link和miniprogram仅会返回一个）
            - text: dict，包括以下字段
                - text.content: 消息文本内容
            - image: dict，包括以下字段
                - image.pic_url: 图片的链接
            - link: dict，包括以下字段
                - link.title: 图文消息标题
                - link.picurl: 图文消息封面的url
                - link.desc: 图文消息的描述
                - link.url: 图文消息的链接
            - miniprogram: dict，包括以下字段
                - miniprogram.title: 小程序消息标题
                - miniprogram.pic_media_id: 小程序消息封面的mediaid
                - miniprogram.appid: 小程序appid
                - miniprogram.page: 小程序page路径
        """
        try:
            return self.post_api(api='group_welcome_template/get', query_params=None,
                                 data={'template_id': template_id})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def del_group_welcome_template(self, template_id: str) -> dict:
        """
        删除群欢迎语素材: 企业可通过此API删除群欢迎语素材
        :param template_id: 群欢迎语素材id
        :return: {}
        """
        try:
            return self.post_api(api='group_welcome_template/del', query_params=None,
                                 data={'template_id': template_id})
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_unassigned_list(self, page_id: int = 0, page_size: int = 1000) -> dict:
        """
        获取离职成员的客户列表: 企业和第三方可通过此接口，获取所有离职成员的客户列表，
        并可进一步调用离职成员的外部联系人再分配接口将这些客户重新分配给其他企业成员。
        :param page_id: 分页查询，要查询页号，从0开始
        :param page_size: 每次返回的最大记录数，默认为1000，最大值为1000
        :return: dict，包括以下字段
            - info: 离职成员信息列表，包括若干个dict，其中字段包括
                - info.handover_userid: 离职成员的userid
                - info.external_userid: 外部联系人userid
                - info.dimission_time: 成员离职时间
            - is_last: 是否是最后一条记录
        注：返回数据按离职时间的降序排列，当page_id为1，page_size为100时，表示取第101到第200条记录
        """
        try:
            data = {'page_id': page_id, "page_size": page_size}
            return self.post_api(api='get_unassigned_list', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def external_contact_transfer(self, external_userid: str, handover_userid: str, takeover_userid: str) -> dict:
        """
        离职成员的外部联系人再分配: 企业可通过此接口，将已离职成员的外部联系人分配给另一个成员接替联系
        :param external_userid: 外部联系人的userid，注意不是企业成员的帐号
                                必须是handover_userid的客户（即配置了客户联系功能的成员所添加的联系人）
        :param handover_userid: 离职成员的userid
        :param takeover_userid: 接替成员的userid
        :return: {}
        错误码40097表示该成员尚未离职，离职成员外部联系人转移接口要求转出用户必须已经离职
        """
        try:
            data = {
                'external_userid': external_userid,
                'handover_userid': handover_userid,
                'takeover_userid': takeover_userid
            }
            return self.post_api(api='transfer', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def groupchat_transfer(self, chat_id_list, new_owner: str) -> dict:
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
        :return: dict，包括以下字段
            - failed_chat_list: 没能成功继承的群的列表，包括若干个dict，其中字段包括
                - failed_chat_list.chat_id: 没能成功继承的群ID
                - failed_chat_list.errcode: 没能成功继承的群，错误码
                - failed_chat_list.errmsg: 没能成功继承的群，错误描述
        错误码40058表示不合法的参数，要求chat_id_list和new_owner不能为空
        错误码46004表示指定的用户new_owner不存在
        错误码90500表示群主并未离职
        错误码90508表示离职群已经继承
        """
        try:
            data = {"chat_id_list": chat_id_list, "new_owner": new_owner}
            return self.post_api(api='groupchat/transfer', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_transfer_result(self, external_userid: str, handover_userid: str, takeover_userid: str) -> dict:
        """
        查询客户接替结果: 企业和第三方可通过此接口查询客户的接替情况
        :param external_userid: 客户的userid，注意不是企业成员的帐号
                                必须是handover_userid的客户（即配置了客户联系功能的成员所添加的联系人）
        :param handover_userid: 转移成员的userid
        :param takeover_userid: 接替成员的userid
        :return: dict，包括以下字段
            - status: 接替状态。1-接替完毕，2-等待接替，3-客户拒绝，4-接替成员客户达到上限，5-无接替记录
            - takeover_time: 接替客户的时间，如果是等待接替状态，则为未来的自动接替时间
        """
        try:
            data = {
                'external_userid': external_userid,
                'handover_userid': handover_userid,
                'takeover_userid': takeover_userid
            }
            return self.post_api(api='get_transfer_result', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_user_behavior_data(self, **data) -> dict:
        """
        获取联系客户统计数据: 企业可通过此接口获取成员联系客户的数据，
        包括发起申请数、新增客户数、聊天数、发送消息数和删除/拉黑成员的客户数等指标
        :param data: dict，包括以下字段
            - userid: 成员ID列表。userid和partyid不可同时为空
            - partyid: 部门ID列表。userid和partyid不可同时为空
            - start_time: 数据起始时间: 时间戳。必须填写
            - end_time: 数据结束时间: 时间戳。必须填写
        :return: dict，包括以下字段
            - behavior_data: list，包括
                - behavior_data.stat_time: 数据日期，为当日0点的时间戳
                - behavior_data.new_apply_cnt: 发起申请数，成员通过「搜索手机号」、「扫一扫」、
                                              「从微信好友中添加」、「从群聊中添加」、「添加共享、分配给我的客户」、
                                              「添加单向、双向删除好友关系的好友」、
                                              「从新的联系人推荐中添加」等渠道主动向客户发起的好友申请数量。
                - behavior_data.new_contact_cnt: 新增客户数，成员新添加的客户数量。
                - behavior_data.chat_cnt: 聊天总数， 成员有主动发送过消息的单聊总数。
                - behavior_data.message_cnt: 发送消息数，成员在单聊中发送的消息总数。
                - behavior_data.reply_percentage: 已回复聊天占比，客户主动发起聊天后，成员在一个自然日内
                                                  有回复过消息的聊天数/客户主动发起的聊天数比例，
                                                  不包括群聊，仅在确有回复时返回。
                - behavior_data.avg_reply_time: 平均首次回复时长，单位为分钟，即客户主动发起聊天后，
                                                成员在一个自然日内首次回复的时长间隔为首次回复时长，
                                                所有聊天的首次回复总时长/已回复的聊天总数即为平均首次回复时长，
                                                不包括群聊，仅在确有回复时返回。
                - behavior_data.negative_feedback_cnt: 删除/拉黑成员的客户数，即将成员删除或加入黑名单的客户数。
        错误码60123表示无效的部门id
        错误码600018表示无效的起始结束时间
        """
        try:
            return self.post_api(api='get_user_behavior_data', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)

    def get_groupchat_data(self, **data) -> dict:
        """
        获取客户群统计数据: 获取指定日期全天的统计数据。注意，企业微信仅存储180天的数据。
        :param data: dict，包括以下字段
            - day_begin_time: 开始时间，填当天开始的0分0秒（否则系统自动处理为当天的0分0秒）。
                              取值范围：昨天至前180天。必须填写
            - owner_filter: 群主过滤: dict。如果不填，表示获取全部群主的数据。包括以下字段
                - userid_list: 群主ID列表。最多100个
                - partyid_list: 群主所属部门ID列表。最多100个
            - order_by: 排序方式。1表示新增群的数量，2表示群总数，3表示新增群人数，4表示群总人数。默认为1
            - order_asc: 是否升序。0表示否；1表示是。默认降序
            - offset: 分页，偏移量，默认为0
            - limit: 分页，预期请求的数据量，默认为500，取值范围为1 ~ 1000
        :return: dict，包括以下字段
            - total: 命中过滤条件的记录总个数
            - next_offset: 当前分页的下一个offset。当next_offset和total相等时，说明已经取完所有
            - items: 记录列表。表示某个群主所拥有的客户群的统计数据。包括
                - owner: 群主ID
                - data: 详情: dict，包括以下字段
                    - new_chat_cnt: 新增客户群数量
                    - chat_total: 截至当天客户群总数量
                    - chat_has_msg: 截至当天有发过消息的客户群数量
                    - new_member_cnt: 客户群新增群人数
                    - member_total: 截至当天客户群总人数
                    - member_has_msg: 截至当天有发过消息的群成员数
                    - msg_total: 截至当天客户群消息总数
        错误码40058表示不合法的参数，要求order_by只能取1、2、3、4，order_asc只能取0、1，limit范围为1 ~ 1000
        错误码60123表示无效的部门id
        错误码600018表示无效的起始结束时间
        """
        try:
            return self.post_api(api='groupchat/statistic', query_params=None, data=data)
        except WeChatWorkSDKException as e:
            raise WeChatWorkSDKException(e.errcode, e.errmsg)
