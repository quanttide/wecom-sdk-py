# -*- coding: utf-8 -*-

from .base import WeChatWorkSDK
from .exception import WeChatWorkSDKException
import re, random, string


class MessageSDK(WeChatWorkSDK):
    def __init__(self, corpid: str, secret: str):
        super().__init__(corpid, secret)

        self.API_ROOT_URL = self.API_ROOT_URL + 'message/'

    def send_message(self, msgtype: str = None, agentid: int = None, touser: str = None, toparty: str = None,
                     totag: str = None, text: dict = None, image: dict = None, voice: dict = None, video: dict = None,
                     file: dict = None, textcard: dict = None, news: dict = None, mpnews: dict = None,
                     markdown: dict = None, miniprogram_notice: dict = None, taskcard: dict = None, safe: int = 0,
                     enable_id_trans: int = 0, enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        推送应用文本、图片、视频、文件、图文等类型。
        :param msgtype: 消息类型
        :param agentid: 企业应用的id，整型
        :param touser: 指定接收消息的成员，成员ID列表，多个接收者用‘|’分隔，最多支持1000个
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个
        :param text:dict 文本消息
        :param image:dict 图片消息
        :param voice:dict 语音消息
        :param video:dict 视频消息
        :param file:dict 文件消息
        :param textcard:dict 文本卡片消息
        :param news:dict 图文消息
        :param mpnews:dict mp图文消息
        :param markdown:dict markdown消息
        :param miniprogram_notice:dict 小程序通知消息
        :param taskcard:dict 任务卡片消息
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_id_trans:int 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :return
            -消息格式正确，请求发送消息
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制touser、toparty、totag参数
        cond_touser = touser and touser.count('|') <= 999
        cond_toparty = toparty and toparty.count('|') <= 99
        cond_totag = totag and toparty.count('|') <= 99

        if touser == '@all':
            pass
        else:
            try:
                assert cond_touser or cond_toparty or cond_totag
            except AssertionError:
                err_message.append('touser、toparty、totag参数错误')

        # 限制msgtype参数
        if msgtype == 'text':
            text_message = TextMessage(msgtype=msgtype, agentid=agentid, text=text, safe=safe,
                                       enable_id_trans=enable_id_trans, enable_duplicate_check=enable_duplicate_check,
                                       duplicate_check_interval=duplicate_check_interval)
            err_message += text_message.text_err()

        elif msgtype == 'image':
            image_message = ImageMessage(msgtype=msgtype, agentid=agentid, image=image, safe=safe,
                                         enable_duplicate_check=enable_duplicate_check,
                                         duplicate_check_interval=duplicate_check_interval)
            err_message += image_message.image_err()

        elif msgtype == 'voice':
            voice_message = VoiceMessage(msgtype=msgtype, agentid=agentid, voice=voice,
                                         enable_duplicate_check=enable_duplicate_check,
                                         duplicate_check_interval=duplicate_check_interval)
            err_message += voice_message.voice_err()

        elif msgtype == 'video':
            video_message = VideoMessage(msgtype=msgtype, agentid=agentid, video=video, safe=safe,
                                         enable_duplicate_check=enable_duplicate_check,
                                         duplicate_check_interval=duplicate_check_interval)
            err_message += video_message.video_err()

        elif msgtype == 'file':
            file_message = FileMessage(msgtype=msgtype, agentid=agentid, file=file, safe=safe,
                                       enable_duplicate_check=enable_duplicate_check,
                                       duplicate_check_interval=duplicate_check_interval)
            err_message += file_message.file_err()

        elif msgtype == 'textcard':
            textcard_message = TextcardMessage(msgtype=msgtype, agentid=agentid, textcard=textcard,
                                               enable_id_trans=enable_id_trans,
                                               enable_duplicate_check=enable_duplicate_check,
                                               duplicate_check_interval=duplicate_check_interval)
            err_message += textcard_message.textcard_err()

        elif msgtype == 'news':
            news_message = NewsMessage(msgtype=msgtype, agentid=agentid, news=news, enable_id_trans=enable_id_trans,
                                       enable_duplicate_check=enable_duplicate_check,
                                       duplicate_check_interval=duplicate_check_interval)
            err_message += news_message.news_err()

        elif msgtype == 'mpnews':
            mpnews_message = MpnewsMessage(msgtype=msgtype, agentid=agentid, mpnews=mpnews, safe=safe,
                                           enable_id_trans=enable_id_trans,
                                           enable_duplicate_check=enable_duplicate_check,
                                           duplicate_check_interval=duplicate_check_interval)
            err_message += mpnews_message.mpnews_err()

        elif msgtype == 'markdown':
            markdown_message = MarkdownMessage(msgtype=msgtype, agentid=agentid, markdown=markdown,
                                               enable_duplicate_check=enable_duplicate_check,
                                               duplicate_check_interval=duplicate_check_interval)
            err_message = markdown_message.markdown_err()

        elif msgtype == 'miniprogram_notice':
            miniprogramnotice_message = MiniprogramnoticeMessage(msgtype=msgtype, miniprogram_notice=miniprogram_notice,
                                                                 enable_id_trans=enable_id_trans,
                                                                 enable_duplicate_check=enable_duplicate_check,
                                                                 duplicate_check_interval=duplicate_check_interval)
            err_message = miniprogramnotice_message.miniprogramnotice_err()

        elif msgtype == 'taskcard':
            taskcard_message = TaskcardMessage(msgtype=msgtype, agentid=agentid, taskcard=taskcard,
                                               enable_id_trans=enable_id_trans,
                                               enable_duplicate_check=enable_duplicate_check,
                                               duplicate_check_interval=duplicate_check_interval)
            err_message += taskcard_message.taskcard_err()

        else:
            err_message.append('msgtype参数错误')

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='send', query_params=dict(),
                                 data={'msgtype': msgtype, 'agentid': agentid, 'touser': touser, 'toparty': toparty,
                                       'totag': totag, 'text': text, 'image': image, 'voice': voice, 'video': video,
                                       'file': file, 'textcard': textcard, 'news': news, 'mpnews': mpnews,
                                       'markdown': markdown, 'miniprogram_notice': miniprogram_notice,
                                       'taskcard': taskcard, 'safe': safe, 'enable_id_trans': enable_id_trans,
                                       'enable_duplicate_check': enable_duplicate_check,
                                       'duplicate_check_interval': duplicate_check_interval})
        else:
            return err_message

    def update_taskcard(self, userids: list = None, agentid: int = None, task_id: str = None, clicked_key: str = None):
        """
        请求更新任务卡片消息
        :param userids: 企业的成员ID列表（消息接收者，最多支持1000个）
        :param agentid: 应用的agentid
        :param task_id: 发送任务卡片消息时指定的task_id
        :param clicked_key: 设置指定的按钮为选择状态，需要与发送消息时指定的btn:key一致
        :return:
            -消息格式正确，请求更新任务卡片
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制agentid参数
        cond_agentid = agentid
        COND[cond_agentid] = '缺少agentid参数'

        # 限制userids参数
        cond_userids = userids and len(userids) <= 1000
        COND[cond_userids] = 'userids参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='update_taskcard', query_params=dict(),
                                 data={'userids': list(userids), 'agentid': agentid, 'task_id': task_id,
                                       'clicked_key': clicked_key})
        else:
            return err_message

    def get_statistics(self, time_type: int = 0):
        """
        查询应用消息发送统计
        :param time_type: 查询哪天的数据，0：当天；1：昨天。默认为0
        :return:
            -消息格式正确，查询应用消息发送统计
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制time_type参数
        cond_time_type = time_type == 1 or time_type == 0
        COND[cond_time_type] = 'time_type参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='get_statistics', query_params=dict(), data={'time_type': time_type})
        else:
            return err_message


class AppchatSDK(WeChatWorkSDK):
    def __init__(self, corpid: str, contact_secret: str):
        super().__init__(corpid, contact_secret)

        self.API_ROOT_URL = self.API_ROOT_URL + 'appchat/'

    def create_appchat(self, userlist: list = None, owner: str = None, chatid: str = None, name: str = None):
        """
        创建群聊会话
        :param userlist: 群成员id列表。至少2人，至多2000人
        :param owner: 指定群主的id。如果不指定，系统会随机从userlist中选一人作为群主
        :param chatid: 群聊的唯一标志，不能与已有的群重复；字符串类型，最长32个字符。
                        只允许字符0-9及字母a-zA-Z。如果不填，系统会随机生成群id
        :param name: 群聊名，最多50个utf8字符，超过将截断
        :return
            -消息格式正确，请求创建群聊会话
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制userlist参数
        userlist = list(userlist)
        cond_userlist = 2 <= len(set(userlist)) <= 2000
        COND[cond_userlist] = 'userlist参数错误'

        # 限制owner参数
        if owner in userlist:
            pass
        else:
            owner = random.choice(userlist)

        # 检查chatid参数，chatid已存在或者未输入chatid则随机生成新的chatid
        if chatid:
            try:
                assert re.match(r'^[0-9a-zA-Z]{1,32}$', chatid)
            except AssertionError:
                chatid_test = True
                while chatid_test:
                    try:
                        self.get_appchat(chatid)
                    except WeChatWorkSDKException:
                        chatid_test = False
                    else:
                        chatid = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 32)))

        else:
            chatid = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 32)))
            chatid_test = True
            while chatid_test:
                try:
                    self.get_appchat(chatid)
                except WeChatWorkSDKException:
                    chatid_test = False
                else:
                    chatid = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 32)))

        # 限制name参数
        if name:
            cond_name = len(name) <= 50
            COND[cond_name] = 'name参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='create', query_params=dict(), data={'userlist': userlist, 'owner': owner,
                                                                          'chatid': chatid, 'name': name})

        else:
            return err_message

    def get_appchat(self, chatid: str = None):
        """
        获取群聊会话
        :param chatid: 群聊id
        :return:
            -消息格式正确，请求获取群聊会话
            -消息格式错误，返回错误信息
        """

        return self.get_api(api='get', query_params={'chatid': chatid})

    def update_appchat(self, chatid: str = None, name: str = None, owner: str = None, add_user_list: list = None,
                       del_user_list: list = None):
        """
        修改群聊会话
        :param chatid: 群聊id
        :param name: 新的群聊名。若不需更新，请忽略此参数。最多50个utf8字符，超过将截断
        :param owner: 新群主的id。若不需更新，请忽略此参数
        :param add_user_list: 添加成员的id列表
        :param del_user_list: 踢出成员的id列表
        :return:
            -消息格式正确，请求修改群聊会话
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检测chatid是否存在
        get_appchat = self.get_appchat(chatid)
        cond_chatid = get_appchat == {}
        COND[cond_chatid] = 'chatid不存在'

        # 获取该chatid信息
        appchat_exist = self.get_appchat(chatid)

        # 限制name参数
        if name:
            cond_name = len(name) <= 200
            COND[cond_name] = 'name参数错误'

        # 限制owner参数
        if owner:
            cond_owner = owner in appchat_exist['chat_info']['userlist']
            COND[cond_owner] = 'owner参数错误'

        # 限制add_user_list参数
        if add_user_list:
            for user in add_user_list:
                cond_add_user_list = 1 <= len(user) <= 64 and len(user) and re.match(r'^[\w][\w@-_.]{1,63}$', user) \
                                     and len(add_user_list) + len(appchat_exist['chat_info']['userlist']) <= 2000
                COND[cond_add_user_list] = 'add_user_list参数错误'

        # 限制del_user_list参数
        if del_user_list:
            for user in del_user_list:
                cond_del_user_list = 1 <= len(user) <= 64 and len(user) and re.match(r'^[\w][\w@-_.]{1,63}$', user) \
                                     and len(del_user_list) <= len(appchat_exist['chat_info']['userlist'])
                COND[cond_del_user_list] = 'del_user_list参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='update', query_params=dict(),
                                 data={'chatid': chatid, 'name': name, 'owner': owner,
                                       'add_user_list': add_user_list,
                                       'del_user_list': del_user_list})
        else:
            return err_message

    def send_appchat(self, chatid: str = None, msgtype: str = None, text: dict = None, image: dict = None,
                     voice: dict = None, video: dict = None, file: dict = None, textcard: dict = None,
                     news: dict = None, mpnews: dict = None, markdown: dict = None, safe: int = 0):
        """
        应用推动消息到群聊会话
        :param chatid:str 群聊id
        :param msgtype:str 消息类型
        :param text:dict 文本消息
        :param image:dict 图片消息
        :param voice:dict 语音消息
        :param video:dict 视频消息
        :param file:dict 文件消息
        :param textcard:dict 文本卡片消息
        :param news:dict 图文消息
        :param mpnews:dict mp图文消息
        :param markdown:dict markdown消息
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :return:
            -消息格式正确，请求应用推送群聊消息
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检测chatid是否存在
        get_appchat = self.get_appchat(chatid)
        cond_chatid = get_appchat == {}
        COND[cond_chatid] = 'chatid不存在'

        # 限制msgtype参数
        if msgtype == 'text':
            text_message = TextMessage(chatid=chatid, msgtype=msgtype, text=text, safe=safe)
            err_message += text_message.text_err()

        elif msgtype == 'image':
            image_message = ImageMessage(chatid=chatid, msgtype=msgtype, image=image, safe=safe)
            err_message += image_message.image_err()

        elif msgtype == 'voice':
            voice_message = VoiceMessage(chatid=chatid, msgtype=msgtype, voice=voice)
            err_message += voice_message.voice_err()

        elif msgtype == 'video':
            video_message = VideoMessage(chatid=chatid, msgtype=msgtype, video=video, safe=safe)
            err_message += video_message.video_err()

        elif msgtype == 'file':
            file_message = FileMessage(chatid=chatid, msgtype=msgtype, file=file, safe=safe)
            err_message += file_message.file_err()

        elif msgtype == 'textcard':
            textcard_message = TextcardMessage(chatid=chatid, msgtype=msgtype, textcard=textcard)
            err_message += textcard_message.textcard_err()

        elif msgtype == 'news':
            news_message = NewsMessage(chatid=chatid, msgtype=msgtype, news=news)
            err_message += news_message.news_err()

        elif msgtype == 'mpnews':
            mpnews_message = MpnewsMessage(chatid=chatid, msgtype=msgtype, mpnews=mpnews, safe=safe)
            err_message += mpnews_message.mpnews_err()

        elif msgtype == 'markdown':
            markdown_message = MarkdownMessage(chatid=chatid, msgtype=msgtype, markdown=markdown)
            err_message += markdown_message.markdown_err()

        else:
            err_message.append('msgtype参数错误')

        # 限制safe参数
        cond_safe = safe == 1 or safe == 0
        COND[cond_safe] = 'safe参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='send', query_params=dict(),
                                 data={'chatid': chatid, 'msgtype': msgtype, 'text': text, 'image': image,
                                       'voice': voice,
                                       'video': video, 'file': file, 'textcard': textcard, 'news': news,
                                       'mpnews': mpnews,
                                       'markdown': markdown, 'safe': safe})
        else:
            return err_message


class LinkedcorpMessageSDK(WeChatWorkSDK):
    def __init__(self, corpid: str, contact_secret: str):
        super().__init__(corpid, contact_secret)

        self.API_ROOT_URL = self.API_ROOT_URL + 'linkedcorp/message/'

    def send_linkedcorpmessage(self, msgtype: str = None, agentid: int = None, toall: int = 0, touser: list = None,
                               toparty: list = None, totag: list = None, text: dict = None, image: dict = None,
                               voice: dict = None, video: dict = None, file: dict = None, textcard: dict = None,
                               news: dict = None, mpnews: dict = None, markdown: dict = None,
                               miniprogram_notice: dict = None, safe: int = 0):
        """
        互联企业发送消息
        :param msgtype:str 消息类型
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param toall:int 1表示发送给应用可见范围内的所有人（包括互联企业的成员），默认为0
        :param touser:list 成员ID列表（消息接收者，最多支持1000个）每个元素的格式为：
                            corpid/userid，其中，corpid为该互联成员所属的企业，userid为该互联成员所属企业中的帐号。
        :param toparty:list 部门ID列表，最多支持100个。partyid在互联圈子内唯一。每个元素都是字符串类型，格式为：
                            linked_id/party_id，其中linked_id是互联id，party_id是在互联圈子中的部门id。
        :param totag:list 本企业的标签ID列表，最多支持100个
        :param text:dict 文本消息
        :param image:dict 图片消息
        :param voice:dict 语音消息
        :param video:dict 视频消息
        :param file:dict 文件消息
        :param textcard:dict 文本卡片消息
        :param news:dict 图文消息
        :param mpnews:dict mp图文消息
        :param markdown:dict markdown消息
        :param miniprogram_notice:dict 小程序通知消息
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :return:
            -消息格式正确，请求发送消息给互联企业
            -消息格式错误，返回错误信息
        """
        # err_message收集格式错误的信息
        err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制toall、touser、toparty、totag参数
        cond_touser = touser and len(touser) <= 1000
        cond_toparty = toparty and len(toparty) <= 100
        cond_totag = totag and len(totag) <= 100

        if toall == 1:
            pass
        else:
            try:
                assert cond_touser or cond_toparty or cond_totag
            except AssertionError:
                err_message.append('touser、toparty、totag参数错误')

        # 限制msgtype参数
        if msgtype == 'text':
            text_message = TextMessage(msgtype=msgtype, agentid=agentid, text=text, safe=safe)
            err_message += text_message.text_err()

        elif msgtype == 'image':
            image_message = ImageMessage(msgtype=msgtype, agentid=agentid, image=image, safe=safe)
            err_message += image_message.image_err()

        elif msgtype == 'voice':
            voice_message = VoiceMessage(msgtype=msgtype, agentid=agentid, voice=voice)
            err_message += voice_message.voice_err()

        elif msgtype == 'video':
            video_message = VideoMessage(msgtype=msgtype, agentid=agentid, video=video, safe=safe)
            err_message += video_message.video_err()

        elif msgtype == 'file':
            file_message = FileMessage(msgtype=msgtype, agentid=agentid, file=file, safe=safe)
            err_message += file_message.file_err()

        elif msgtype == 'textcard':
            textcard_message = TextcardMessage(msgtype=msgtype, agentid=agentid, textcard=textcard)
            err_message += textcard_message.textcard_err()

        elif msgtype == 'news':
            news_message = NewsMessage(msgtype=msgtype, agentid=agentid, news=news)
            err_message += news_message.news_err()

        elif msgtype == 'mpnews':
            mpnews_message = MpnewsMessage(msgtype=msgtype, agentid=agentid, mpnews=mpnews, safe=safe)
            err_message += mpnews_message.mpnews_err()

        elif msgtype == 'markdown':
            markdown_message = MarkdownMessage(msgtype=msgtype, agentid=agentid, markdown=markdown)
            err_message += markdown_message.markdown_err()

        elif msgtype == 'miniprogram_notice':
            miniprogramnotice_message = MiniprogramnoticeMessage(msgtype=msgtype, miniprogram_notice=miniprogram_notice)
            err_message += miniprogramnotice_message.miniprogramnotice_err()

        else:
            err_message.append('msgtype参数错误')

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                err_message.append(COND[cond])

        if not err_message:
            return self.post_api(api='send', query_params=dict(),
                                 data={'msgtype': msgtype, 'agentid': agentid, 'toall': toall, 'touser': touser,
                                       'toparty': toparty, 'totag': totag, 'text': text, 'image': image, 'voice': voice,
                                       'video': video, 'file': file, 'textcard': textcard, 'news': news,
                                       'mpnews': mpnews,
                                       'markdown': markdown, 'miniprogram_notice': miniprogram_notice, 'safe': safe})
        else:
            return err_message


class Message(object):
    def __init__(self, msgtype: str = None):
        """
        :param msgtype:str 消息类型
        """
        self.msgtype = msgtype


class TextMessage(Message):

    def __init__(self, msgtype: str = 'text', agentid: int = None, chatid: str = None, text: dict = None,
                 safe: int = 0, enable_id_trans: int = 0, enable_duplicate_check: int = 0,
                 duplicate_check_interval: int = 1800):
        """
        文本消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param text:dict
            -content:str 消息内容，最长不超过2048个字节，超过将截断（支持id转译）
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_id_trans:int 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.text = text
        self.safe = safe
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def text_err(self):
        # err_message收集格式错误的信息
        text_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            text_err_message.append('agentid或chatid不存在')

        # 限制content参数
        cond_content = not (not self.text or not ('content' in self.text) or not self.text['content'] or not (
                len(self.text['content']) <= 2048))
        COND[cond_content] = 'content参数错误'

        # 限制safe参数
        cond_safe = self.safe == 1 or self.safe == 0
        COND[cond_safe] = 'safe参数错误'

        # 限制enable_id_trans参数
        cond_enable_id_trans = self.enable_id_trans == 1 or self.enable_id_trans == 0
        COND[cond_enable_id_trans] = 'enable_id_trans参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                text_err_message.append(COND[cond])

        return text_err_message


class ImageMessage(Message):

    def __init__(self, msgtype: str = 'image', agentid: int = None, chatid: str = None, image: dict = None,
                 safe: int = 0,
                 enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        图片消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param image:dict
            -media_id:str 图片媒体文件id，可以调用上传临时素材接口获取
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.image = image
        self.safe = safe
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def image_err(self):
        # err_message收集格式错误的信息
        image_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            image_err_message.append('agentid或chatid不存在')

        # 限制media_id参数
        cond_media_id = not (not self.image or not ('media_id' in self.image) or not self.image['media_id'])
        COND[cond_media_id] = 'media_id参数错误'

        # 限制safe参数
        cond_safe = self.safe == 1 or self.safe == 0
        COND[cond_safe] = 'safe参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                image_err_message.append(COND[cond])

        return image_err_message


class VoiceMessage(Message):

    def __init__(self, msgtype: str = 'voice', agentid: int = None, chatid: str = None, voice: dict = None,
                 enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        语音消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param voice:dict
            -media_id:str 语音文件id，可以调用上传临时素材接口获取
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.voice = voice
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def voice_err(self):
        # err_message收集格式错误的信息
        voice_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            voice_err_message.append('agentid或chatid不存在')

        # 限制media_id参数
        cond_media_id = self.voice and 'media_id' in self.voice and self.voice['media_id']
        COND[cond_media_id] = 'media_id参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                voice_err_message.append(COND[cond])

        return voice_err_message


class VideoMessage(Message):

    def __init__(self, msgtype: str = 'video', agentid: int = None, chatid: str = None, video: dict = None,
                 safe: int = 0, enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        视频消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param video:dict
            -media_id:str 视频媒体文件id，可以调用上传临时素材接口获取
            -title:str 视频消息的标题，不超过128个字节，超过会自动截断
            -description:str 视频消息的描述，不超过512个字节，超过会自动截断
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时,
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.video = video
        self.safe = safe
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def video_err(self):
        # err_message收集格式错误的信息
        video_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            video_err_message.append('agentid或chatid不存在')

        # 限制video参数
        if self.video:

            # 限制media_id参数
            cond_media_id = 'media_id' in self.video and self.video['media_id']
            COND[cond_media_id] = 'media_id参数错误'

            # 限制title参数
            if 'title' in self.video:
                cond_video_title = len(self.video['title']) <= 128
                COND[cond_video_title] = 'title参数错误'

            # 限制description参数
            if 'description' in self.video:
                cond_video_description = len(self.video['description']) <= 512
                COND[cond_video_description] = 'description参数错误'

        else:
            cond_video = self.video
            COND[cond_video] = '缺少video参数'

        # 限制safe参数
        cond_safe = self.safe == 1 or self.safe == 0
        COND[cond_safe] = 'safe参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                video_err_message.append(COND[cond])

        return video_err_message


class FileMessage(Message):

    def __init__(self, msgtype: str = 'file', agentid: int = None, chatid: str = None, file: dict = None, safe: int = 0,
                 enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        文本消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param file:dict
            -media_id:str 文件id，可以调用上传临时素材接口获取
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.file = file
        self.safe = safe
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def file_err(self):
        # err_message收集格式错误的信息
        file_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            file_err_message.append('agentid或chatid不存在')

        # 限制media_id参数
        cond_media_id = self.file and 'media_id' in self.file and self.file['media_id']
        COND[cond_media_id] = 'media_id参数错误'

        # 限制safe参数
        cond_safe = self.safe == 1 or self.safe == 0
        COND[cond_safe] = 'safe参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                file_err_message.append(COND[cond])

        return file_err_message


class TextcardMessage(Message):

    def __init__(self, msgtype: str = 'textcard', agentid: int = None, chatid: str = None, textcard: dict = None,
                 enable_id_trans: int = 0, enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        文本卡片消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param textcard:dict
            -title:str 标题，不超过128个字节，超过会自动截断（支持id转译）
            -description:str 描述，不超过512个字节，超过会自动截断（支持id转译）
            -url:str 点击后跳转的链接
            -btntxt:str 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断
        :param enable_id_trans:int 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.textcard = textcard
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def textcard_err(self):
        # err_message收集格式错误的信息
        textcard_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            textcard_err_message.append('agentid或chatid不存在')

        # 限制textcard参数
        if self.textcard:

            # 限制title参数
            cond_textcard_title = 'title' in self.textcard and self.textcard['title'] and \
                                  len(self.textcard['title']) <= 128
            COND[cond_textcard_title] = 'title参数错误'

            # 限制description参数
            cond_textcard_description = 'description' in self.textcard and self.textcard['description'] and \
                                        len(self.textcard['description']) <= 512
            COND[cond_textcard_description] = 'description参数错误'

            # 限制url参数
            cond_textcard_url = 'url' in self.textcard and self.textcard['url']
            COND[cond_textcard_url] = '缺少url参数'

            # 限制btntxt参数
            if 'btntxt' in self.textcard:
                cond_textcard_btntxt = self.textcard['btntxt'] and len(self.textcard['btntxt']) <= 4
                COND[cond_textcard_btntxt] = 'btntxt参数错误'

        else:
            cond_textcard = self.textcard
            COND[cond_textcard] = '缺少textcard参数'

        # 限制enable_id_trans参数
        cond_enable_id_trans = self.enable_id_trans == 1 or self.enable_id_trans == 0
        COND[cond_enable_id_trans] = 'enable_id_trans参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                textcard_err_message.append(COND[cond])

        return textcard_err_message


class NewsMessage(Message):

    def __init__(self, msgtype: str = 'news', agentid: int = None, chatid: str = None, news: dict = None,
                 enable_id_trans: int = 0,
                 enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        图文消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param news:dict
            -articles:list 图文消息，一个图文消息支持1到8条图文
                -title:str 标题，不超过128个字节，超过会自动截断（支持id转译）
                -description:str 描述，不超过512个字节，超过会自动截断（支持id转译）
                -url:str 点击后跳转的链接
                -picurl:str 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150
        :param enable_id_trans:int 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.news = news
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def news_err(self):
        # err_message收集格式错误的信息
        news_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            news_err_message.append('agentid或chatid不存在')

        # 限制news、articles参数
        cond_articles = self.news and 'articles' in self.news and self.news['articles'] \
                        and len(self.news['articles']) <= 8
        COND[cond_articles] = 'articles参数错误'

        if cond_articles:
            # 限制title、url、description、picurl参数
            for article in self.news['articles']:
                cond_news_title = 'title' in article and article['title'] and len(article['title']) <= 128
                COND[cond_news_title] = 'title参数错误'

                cond_news_url = 'url' in article and article['url']
                COND[cond_news_url] = 'url参数错误'

                if 'description' in article:
                    cond_news_description = article['description'] and len(article['description']) <= 512
                    COND[cond_news_description] = 'description参数错误'

                if 'picurl' in article:
                    cond_news_picurl = article['picurl']
                    COND[cond_news_picurl] = 'picurl参数错误'

        # 限制enable_id_trans参数
        cond_enable_id_trans = self.enable_id_trans == 1 or self.enable_id_trans == 0
        COND[cond_enable_id_trans] = 'enable_id_trans参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                news_err_message.append(COND[cond])

        return news_err_message


class MpnewsMessage(Message):

    def __init__(self, msgtype: str = 'mpnews', agentid: int = None, chatid: str = None, mpnews: dict = None,
                 safe: int = 0, enable_id_trans: int = 0, enable_duplicate_check: int = 0,
                 duplicate_check_interval: int = 1800):
        """
        mpnews图文消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param mpnews:dict
            -articles:list 图文消息，一个图文消息支持1到8条图文
                -title:str 标题，不超过128个字节，超过会自动截断（支持id转译）
                -thumb_media_id:str 图文消息缩略图的media_id, 可以通过素材管理接口获得。此处thumb_media_id即上传接口返回的media_id
                -author:str 图文消息的作者，不超过64个字节
                -content_source_url:str 图文消息点击“阅读原文”之后的页面链接
                -content:str 图文消息的内容，支持html标签，不超过666K个字节（支持id转译）
                -digest:str 图文消息的描述，不超过512个字节，超过会自动截断
        :param safe:int 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_id_trans:int 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.mpnews = mpnews
        self.safe = safe
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def mpnews_err(self):
        # err_message收集格式错误的信息
        mpnews_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            mpnews_err_message.append('agentid或chatid不存在')

        # 限制articles参数
        cond_articles = self.mpnews and 'articles' in self.mpnews and self.mpnews['articles'] and \
                        len(self.mpnews['articles']) <= 8
        COND[cond_articles] = 'articles参数错误'

        # 限制title、thumb_media_id、author、content_source_url、content、digest参数
        if cond_articles:
            for article in self.mpnews['articles']:
                cond_mpnews_title = 'title' in article and article['title'] and len(article['title']) <= 128
                COND[cond_mpnews_title] = 'title参数错误'

                cond_mpnews_thumb_media_id = 'thumb_media_id' in article and article['thumb_media_id']
                COND[cond_mpnews_thumb_media_id] = '缺少thumb_media_id参数'

                cond_mpnews_content = 'content' in article and article['content'] and len(article['content']) <= 666000
                COND[cond_mpnews_content] = 'content参数错误'

                if 'content_source_url' in article:
                    cond_mpnews_content_source_url = article['content_source_url']
                    COND[cond_mpnews_content_source_url] = 'content_source_url参数错误'

                if 'author' in article:
                    cond_mpnews_author = article['author'] and len(article['author']) <= 64
                    COND[cond_mpnews_author] = 'author参数错误'

                if 'digest' in article:
                    cond_mpnews_digest = article['digest'] and len(article['digest']) <= 512
                    COND[cond_mpnews_digest] = 'digest参数错误'

        # 限制safe参数
        cond_safe = self.safe == 2 or self.safe == 1 or self.safe == 0
        COND[cond_safe] = 'safe参数错误'

        # 限制enable_id_trans参数
        cond_enable_id_trans = self.enable_id_trans == 1 or self.enable_id_trans == 0
        COND[cond_enable_id_trans] = 'enable_id_trans参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                mpnews_err_message.append(COND[cond])

        return mpnews_err_message


class MarkdownMessage(Message):

    def __init__(self, msgtype: str = 'markdown', agentid: int = None, chatid: str = None, markdown: dict = None,
                 enable_duplicate_check: int = 0,
                 duplicate_check_interval: int = 1800):
        """
        markdown消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param chatid:str 群聊id
        :param markdown:dict
            -content: markdown内容，最长不超过2048个字节，必须是utf8编码
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.chatid = chatid
        self.markdown = markdown
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def markdown_err(self):
        # err_message收集格式错误的信息
        markdown_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 检查是否有agentid、chatid参数
        if self.agentid:
            pass
        elif self.chatid:
            pass
        else:
            markdown_err_message.append('agentid或chatid不存在')

        # 限制content参数
        cond_markdown_content = not (
                not self.markdown or not ('content' in self.markdown) or not self.markdown['content'] or not (
                len(self.markdown['content']) <= 2048))
        COND[cond_markdown_content] = 'content参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                markdown_err_message.append(COND[cond])

        return markdown_err_message


class MiniprogramnoticeMessage(Message):

    def __init__(self, msgtype: str = 'miniprogram_notice', miniprogram_notice: dict = None, enable_id_trans: int = 0,
                 enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        小程序通知消息
        :param miniprogram_notice:dict
            -appid:str 小程序appid，必须是与当前小程序应用关联的小程序
            -title:str 消息标题，长度限制4-12个汉字（支持id转译）
            -page:str 点击消息卡片后的小程序页面，仅限本小程序内的页面。该字段不填则消息点击后不跳转
            -description:str 消息描述，长度限制4-12个汉字（支持id转译）
            -emphasis_first_item:bool 是否放大第一个content_item
            -content_item:list
                -key: 长度10个汉字以内
                -value: 长度30个汉字以内（支持id转译）
        :param enable_id_trans: 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.miniprogram_notice = miniprogram_notice
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def miniprogramnotice_err(self):
        # err_message收集格式错误的信息
        miniprogramnotice_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制miniprogram_notice参数
        if self.miniprogram_notice:

            # 限制appid参数
            cond_miniprogram_notice_appid = 'appid' in self.miniprogram_notice and self.miniprogram_notice['appid']
            COND[cond_miniprogram_notice_appid] = 'appid参数错误'

            # 限制title参数
            cond_miniprogram_notice_title = 'title' in self.miniprogram_notice and self.miniprogram_notice['title'] \
                                            and 4 <= len(self.miniprogram_notice['title']) <= 12
            COND[cond_miniprogram_notice_title] = 'title参数错误'

            # 限制page参数
            if 'page' in self.miniprogram_notice:
                cond_miniprogram_notice_page = self.miniprogram_notice['page']
                COND[cond_miniprogram_notice_page] = 'page参数错误'

            # 限制description参数
            if 'description' in self.miniprogram_notice:
                cond_miniprogram_notice_description = self.miniprogram_notice['description'] \
                                                      and 4 <= len(self.miniprogram_notice['description']) <= 12
                COND[cond_miniprogram_notice_description] = 'description参数错误'

            # 限制content_item参数
            if 'content_item' in self.miniprogram_notice:
                cond_miniprogram_notice_content_item = self.miniprogram_notice['content_item'] \
                                                       and len(self.miniprogram_notice['content_item']) <= 10
                COND[cond_miniprogram_notice_content_item] = 'content_item参数错误'

                if self.miniprogram_notice['content_item']:
                    # 限制key、value参数
                    for item in self.miniprogram_notice['content_item']:
                        cond_miniprogram_notice_key = 'key' in item and item['key'] and len(item['key']) <= 10
                        COND[cond_miniprogram_notice_key] = 'key参数错误'

                        cond_miniprogram_notice_value = 'value' in item and item['value'] and len(item['value']) <= 30
                        COND[cond_miniprogram_notice_value] = 'value参数错误'
        else:
            cond_miniprogram_notice = self.miniprogram_notice
            COND[cond_miniprogram_notice] = 'miniprogram参数错误'

        # 限制enable_id_trans参数
        cond_enable_id_trans = self.enable_id_trans == 1 or self.enable_id_trans == 0
        COND[cond_enable_id_trans] = 'enable_id_trans参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                miniprogramnotice_err_message.append(COND[cond])

        return miniprogramnotice_err_message


class TaskcardMessage(Message):

    def __init__(self, msgtype: str = 'taskcard', agentid: int = None, taskcard: dict = None, enable_id_trans: int = 0,
                 enable_duplicate_check: int = 0, duplicate_check_interval: int = 1800):
        """
        任务卡片消息
        :param agentid:int 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        :param taskcard:dict
            -title:str 标题，不超过128个字节，超过会自动截断（支持id转译）
            -description:str 描述，不超过512个字节，超过会自动截断（支持id转译）
            -task_id:str 任务id，同一个应用发送的任务卡片消息的任务id不能重复，只能由数字、字母和“_-@”组成，最长支持128字节
            -url:str 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
            -btn:list 按钮列表，按钮个数为1~2个
                -key:str 按钮key值，用户点击后，会产生任务卡片回调事件，回调事件会带上该key值，只能由数字、字母和“_-@”组成，
                    最长支持128字节
                -name:str 按钮名称
                -replace_name:str 点击按钮后显示的名称，默认为“已处理”
                -color:str 按钮字体颜色，可选“red”或者“blue”,默认为“blue”
                -is_bold:bool 按钮字体是否加粗，默认false
        :param enable_id_trans:int 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check:int 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval:int 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        """
        super().__init__(msgtype)
        self.agentid = agentid
        self.taskcard = taskcard
        self.enable_id_trans = enable_id_trans
        self.enable_duplicate_check = enable_duplicate_check
        self.duplicate_check_interval = duplicate_check_interval

    def taskcard_err(self):
        # err_message收集格式错误的信息
        taskcard_err_message = []

        # COND存放正常的信息状况
        COND = {}

        # 限制agentid参数
        cond_taskcard_agentid = self.agentid is not None
        COND[cond_taskcard_agentid] = 'agentid参数错误'

        # 限制taskcard参数
        if self.taskcard:

            # 限制title参数
            cond_taskcard_title = 'title' in self.taskcard and self.taskcard['title'] and \
                                  len(self.taskcard['title']) <= 128
            COND[cond_taskcard_title] = 'title参数错误'

            # 限制description参数
            cond_taskcard_description = 'description' in self.taskcard and self.taskcard['description'] and \
                                        len(self.taskcard['description']) <= 512
            COND[cond_taskcard_description] = 'description参数错误'

            # 限制url参数
            if 'url' in self.taskcard:
                cond_taskcard_url = self.taskcard['url'] and len(self.taskcard['url']) <= 2048 and \
                                    (self.taskcard['url'].startswith('https') or self.taskcard['url'].startswith('http'))
                COND[cond_taskcard_url] = 'url参数错误'

            # 限制task_id参数
            cond_taskcard_task_id = 'task_id' in self.taskcard and self.taskcard['task_id'] and \
                                    re.match(r'^[\w@-_]{1,128}$', self.taskcard['task_id'])
            COND[cond_taskcard_task_id] = 'task_id参数错误'

            # 限制btn参数
            cond_taskcard_btn = 'btn' in self.taskcard and self.taskcard['btn'] and len(self.taskcard['btn']) <= 2
            COND[cond_taskcard_btn] = 'btn参数错误'

            # 限制key、name、color参数
            for btn in self.taskcard['btn']:
                cond_taskcard_btn_key = 'key' in btn and btn['key'] and re.match(r'^[\w@-_]{1,128}$', btn['key'])
                COND[cond_taskcard_btn_key] = 'btn:key参数错误'

                cond_taskcard_btn_name = 'name' in btn and btn['name']
                COND[cond_taskcard_btn_name] = 'btn:name参数错误'

                if 'color' in btn:
                    cond_taskcard_btn_color = btn['color'] == 'red' or btn['color'] == 'blue'
                    COND[cond_taskcard_btn_color] = 'btn:color参数错误'
        else:
            cond_taskcard = self.taskcard
            COND[cond_taskcard] = 'taskcard参数错误'

        # 限制enable_id_trans参数
        cond_enable_id_trans = self.enable_id_trans == 1 or self.enable_id_trans == 0
        COND[cond_enable_id_trans] = 'enable_id_trans参数错误'

        # 限制enable_duplicate_check参数
        cond_enable_duplicate_check = self.enable_duplicate_check == 1 or self.enable_duplicate_check == 0
        COND[cond_enable_duplicate_check] = 'enable_duplicate_check参数错误'

        # 限制duplicate_check_interval参数
        cond_duplicate_check_interval = self.duplicate_check_interval <= 14400
        COND[cond_duplicate_check_interval] = 'duplicate_check_interval参数错误'

        for cond in COND:
            try:
                assert cond
            except AssertionError:
                taskcard_err_message.append(COND[cond])

        return taskcard_err_message
