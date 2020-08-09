from .base import WeChatWorkSDK, WECHATWORK_API_ROOT_URL, get_access_token
from .exception import WeChatWorkSDKException
import re, random, string

class MessageSDK(WeChatWorkSDK):
    def __init__(self, corpid, secret):
        super().__init__(corpid, secret)

        self.API_ROOT_URL = self.API_ROOT_URL + 'message/'


    def sendmessage(self, msgtype, safe=0, enable_id_trans=0, enable_duplicate_check=0, \
                    duplicate_check_interval=1800, btntxt='详情', **kwargs):
        """

        :param msgtype: 消息类型
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0
        :param enable_id_trans: 表示是否开启id转译，0表示否，1表示是，默认0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs:
            -touser: 指定接收消息的成员，成员ID列表，多个接收者用‘|’分隔，最多支持1000个
            -toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个
            -totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个
            -
        :return: 发送应用消息
        """
        # 限制touser、toparty、totag参数
        if 'touser' in kwargs:
            if kwargs['touser'] == '@all':
                pass

            elif kwargs['touser'].count('|') <= 999:
                if 'toparty' in kwargs and kwargs['toparty']:
                    assert kwargs['toparty'].count('|') <= 99
                if 'totag' in kwargs and kwargs['totag']:
                    assert kwargs['totag'].count('|') <= 99
            else:
                raise AssertionError

        elif 'toparty' in kwargs and kwargs['toparty']:
            if kwargs['toparty'].count('|') <= 99:
                if 'totag' in kwargs and kwargs['totag']:
                    assert kwargs['totag'].count('|') <= 99
            else:
                raise AssertionError

        elif 'totag' in kwargs and kwargs['totag']:
            if kwargs['totag'].count('|') <= 99:
                pass
            else:
                raise AssertionError

        else:
            raise AssertionError

        # 限制safe参数
        if safe == 1 or safe == 0:
            pass
        else:
            raise AssertionError

        # 限制enable_id_trans参数
        if enable_id_trans == 1 or enable_id_trans == 0:
            pass
        else:
            raise AssertionError

        # 限制enable_duplicate_check参数
        if enable_duplicate_check == 1 or enable_duplicate_check == 0:
            pass
        else:
            raise AssertionError

        # 限制duplicate_check_interval参数
        if duplicate_check_interval <= 14400:
            pass
        else:
            raise AssertionError

        # 其余参数放入messagelist进行限制，参数错误返回False
        assert messagelist(msgtype=msgtype, **kwargs)

        return self.post_api(api='send', query_params=dict(),
                             data={'msgtype': msgtype, 'safe':safe, 'enable_id_trans':enable_id_trans,
                                   'enable_duplicate_check':enable_duplicate_check, 'duplicate_check_interval':duplicate_check_interval,
                                   'btntxt':btntxt, **kwargs})

    def update_taskcard(self, userids, agentid, task_id, clicked_key):
        """

        :param userids: 企业的成员ID列表（消息接收者，最多支持1000个）
        :param agentid: 应用的agentid
        :param task_id: 发送任务卡片消息时指定的task_id
        :param clicked_key: 设置指定的按钮为选择状态，需要与发送消息时指定的btn:key一致
        :return: 请求更新任务卡片消息
        """

        # 限制agentid参数不为None
        assert agentid

        # 限制userids参数
        if userids:
            assert len(userids) <= 1000

        return self.post_api(api='update_taskcard', query_params=dict(),
                             data={'userids':list(userids), 'agentid':agentid, 'task_id':task_id, 'clicked_key':clicked_key})

    def get_statistics(self, **kwargs):
        """

        :param kwargs:
            -time_type: 查询哪天的数据，0：当天；1：昨天。默认为0
        :return: 查询应用消息发送统计
        """
        if kwargs['time_type']:
            assert kwargs['time_type'] == 1 or kwargs['time_type'] == 0

        message = self.post_api(api='get_statistics', query_params=dict(), data=(kwargs))
        print(message)

class AppchatSDK(WeChatWorkSDK):
    def __init__(self, corpid, contact_secret):
        super().__init__(corpid, contact_secret)

        self.API_ROOT_URL = self.API_ROOT_URL + 'appchat/'

    def create_appchat(self, userlist, owner=None, chatid=None, **kwargs):
        """
        创建群聊会话

        :param userlist: 群成员id列表。至少2人，至多2000人
        :param owner: 指定群主的id。如果不指定，系统会随机从userlist中选一人作为群主
        :param chatid: 群聊的唯一标志，不能与已有的群重复；字符串类型，最长32个字符。只允许字符0-9及字母a-zA-Z。如果不填，系统会随机生成群id
        :param kwargs:
            -name: 群聊名，最多50个utf8字符，超过将截断
        """
        # 限制userlist参数
        if userlist:
            userlist = list(userlist)
            assert len(set(userlist)) <= 2000 and len(set(userlist)) >= 2

        #限制owner参数
        if owner:
            pass
        else:
            owner = random.choice(userlist)

        # 检查chatid参数，chatid已存在或者未输入chatid则随机生成新的chatid
        if chatid:
            assert re.match(r'^[0-9a-zA-Z]{1,32}$', chatid)
            chatid_test = True
            while chatid_test:
                try:
                    self.get_appchat(chatid)
                except WeChatWorkSDKException:
                    chatid_test = False
                else:
                    chatid = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 32)))

        else:
            chatid = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1,32)))
            chatid_test = True
            while chatid_test:
                try:
                    self.get_appchat(chatid)
                except WeChatWorkSDKException:
                    chatid_test = False
                else:
                    chatid = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1, 32)))

        # 限制name参数
        if 'name' in kwargs and kwargs['name']:
            assert len(kwargs['name']) <= 4*50

        appchat_info = self.post_api(api='create', query_params=dict(), data={'userlist':userlist, 'owner':owner,
                                                                     'chatid':chatid, **kwargs})
        # 群聊创建成功，显示信息
        print(appchat_info)

    def get_appchat(self, chatid):
        """

        :param chatid: 群聊id
        :return: 获取群聊会话
        """
        return self.get_api(api='get', query_params={'chatid':chatid})

    def update_appchat(self, chatid, **kwargs):
        """

        :param chatid: 群聊id
        :param kwargs:
            -name: 新的群聊名。若不需更新，请忽略此参数。最多50个utf8字符，超过将截断
            -owner: 新群主的id。若不需更新，请忽略此参数
            -add_user_list: 添加成员的id列表
            -del_user_list: 踢出成员的id列表
        :return:
        """

        # 检测chatid是否存在
        assert self.get_appchat(chatid)

        # 获取该chatid信息
        appchat_exist = self.get_appchat(chatid)

        # 限制add_user_list参数
        if 'add_user_list' in kwargs and kwargs['add_user_list']:
            for user in kwargs['add_user_list']:
                assert len(user) <= 64 and len(user) >= 1
                assert re.match(r'^[\w][\w@-_.]{1,63}$', user)
            assert len(kwargs['add_user_list']) + len(appchat_exist['chat_info']['userlist']) <= 2000

        # 限制del_user_list参数
        if 'del_user_list' in kwargs and kwargs['del_user_list']:
            for user in kwargs['del_user_list']:
                assert len(user) <= 64 and len(user) >= 1
                assert re.match(r'^[\w][\w@-_.]{1,63}$', user)
            assert set(kwargs['del_user_list']) < set(appchat_exist)

        # 限制name参数
        if 'name' in kwargs and kwargs['name']:
            assert len(kwargs['name']) <= 4 * 50

        return self.post_api(api='update', query_params=dict(), data={'chatid':chatid, **kwargs})

    def send_appchat(self, chatid, msgtype, safe=0, **kwargs):
        """

        :param chatid: 	群聊id
        :param msgtype: 消息类型
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0
        :param kwargs:
        :return: 应用推动消息到群聊会话
        """

        # 检查chatid是否存在
        assert self.get_appchat(chatid)

        # 限制safe参数
        if safe == 1 or safe == 0:
            pass
        else:
            raise AssertionError

        # 限制msgtype参数
        if msgtype == 'miniprogram_notice':
            raise AssertionError
        if msgtype == 'taskcard':
            raise AssertionError

        # 其余参数放入messagelist进行限制，参数错误返回False
        assert messagelist(msgtype=msgtype, chatid=chatid, **kwargs)

        return self.post_api(api='send', query_params=dict(), data={'chatid':chatid, 'msgtype':msgtype,
                                                                    'safe':safe, **kwargs})



class LinkedcorpMessageSDK(WeChatWorkSDK):
    def __init__(self, corpid, contact_secret):
        super().__init__(corpid, contact_secret)

        self.API_ROOT_URL = self.API_ROOT_URL + 'linkedcorp/message/'

    def send_linkedcorpmessage(self, msgtype, toall=0, safe=0, **kwargs):
        """

        :param msgtype: 消息类型
        :param toall: 1表示发送给应用可见范围内的所有人（包括互联企业的成员），默认为0
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0
        :param kwargs:
            -touser: 指定接收消息的成员，成员ID列表，多个接收者用‘|’分隔，最多支持1000个
            -toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个
            -totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个
        :return: 互联企业发送消息
        """

        # 限制toall、touser、toparty、totag参数
        if toall == 1:
            pass

        elif toall == 0:
            if 'touser' in kwargs and kwargs['touser']:
                assert len(kwargs['touser']) <= 1000
                if 'toparty' in kwargs and kwargs['toparty']:
                    assert len(kwargs['toparty']) <= 100
                if 'totag' in kwargs and kwargs['totag']:
                    assert len(kwargs['totag']) <= 100

            elif 'toparty' in kwargs and kwargs['toparty']:
                assert len(kwargs['toparty']) <= 100
                if 'totag' in kwargs and kwargs['totag']:
                    assert len(kwargs['totag']) <= 100

            elif 'totag' in kwargs and kwargs['totag']:
                assert len(kwargs['totag']) <= 100

            else:
                raise AssertionError

        else:
            raise AssertionError

        # 限制safe参数
        if safe == 1 or safe == 0:
            pass
        else:
            raise AssertionError

        # 其余参数放入messagelist进行限制，参数错误返回False
        assert messagelist(msgtype=msgtype, **kwargs)

        return self.post_api(api='send', query_params=dict(), data={'msgtype':msgtype, 'toall':toall, 'safe':safe, **kwargs})



def messagelist(msgtype, chatid=None, **kwargs):
    """

    :param msgtype: 消息类型
    :param kwargs:
        -touser: 指定接收消息的成员，成员ID列表，多个接收者用‘|’分隔，最多支持1000个
        -toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个
        -totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个
        -agentid: 企业应用的id，整型。企业内部开发，可在应用的设置页面查看
        -content: 消息内容，最长不超过2048个字节，超过将截断
        -media_id: 图片媒体文件id，可以调用上传临时素材接口获取
        -title: 视频消息的标题，不超过128个字节，超过会自动截断
        -description: 视频消息的描述，不超过512个字节，超过会自动截断
        -url: 点击后跳转的链接
        -btntxt: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断
        -articles: 图文消息，一个图文消息支持1到8条图文
        -picurl: 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150
        -thumb_media_id: 图文消息缩略图的media_id, 可以通过素材管理接口获得。此处thumb_media_id即上传接口返回的media_id
        -author: 图文消息的作者，不超过64个字节
        -content_source_url: 图文消息点击“阅读原文”之后的页面链接
        -digest: 图文消息的描述，不超过512个字节，超过会自动截断
        -appid: 小程序appid，必须是与当前小程序应用关联的小程序
        -page: 点击消息卡片后的小程序页面，仅限本小程序内的页面。该字段不填则消息点击后不跳转
        -emphasis_first_item: 是否放大第一个content_item
        -content_item: 消息内容键值对，最多允许10个item
        -key: 长度10个汉字以内
        -value: 长度30个汉字以内
        -task_id: 任务id，同一个应用发送的任务卡片消息的任务id不能重复，只能由数字、字母和“_-@”组成，最长支持128字节
        -btn: 按钮列表，按钮个数为1~2个
        -btn:key: 按钮key值，用户点击后，会产生任务卡片回调事件，回调事件会带上该key值，只能由数字、字母和“_-@”组成，
            最长支持128字节
        -btn:name: 按钮名称
        -btn:replace_name: 点击按钮后显示的名称，默认为“已处理”
        -btn:color: 按钮字体颜色，可选“red”或者“blue”,默认为“blue”
        -btn:is_bold: 按钮字体是否加粗，默认false

    :return: 消息参数正确返回Ture，消息参数错误返回False
    """
    messagecorrect = True

    #文本消息
    if msgtype == 'text':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid !=None:
            pass
        else:
            messagecorrect = False

        if 'text' in kwargs and kwargs['text']:
            if 'content' in kwargs['text'] and kwargs['text']['content']:
                if len(kwargs['text']['content']) <= 2048:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False
        else:
            messagecorrect = False

    #图片消息
    elif msgtype == 'image':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid !=None:
            pass
        else:
            messagecorrect = False

        if 'image' in kwargs and kwargs['image']:
            if 'media_id' in kwargs['image'] and kwargs['image']['media_id']:
                pass
            else:
                messagecorrect = False
        else:
            messagecorrect = False

    #语音消息
    elif msgtype == 'voice':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if 'voice' in kwargs and kwargs['voice']:
            if 'media_id' in kwargs['voice'] and kwargs['voice']['media_id']:
                pass
            else:
                messagecorrect = False
        else:
            messagecorrect = False

    #视频消息
    elif msgtype == 'video':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if 'video' in kwargs and kwargs['video']:
            if 'media_id' in kwargs['video'] and kwargs['video']['media_id']:
                pass
            else:
                messagecorrect = False

            if 'title' in kwargs['video'] and kwargs['video']['title']:
                if len(kwargs['video']['title']) <= 128:
                    pass
                else:
                    messagecorrect = False

            if 'description' in kwargs['video'] and kwargs['video']['description']:
                if len(kwargs['video']['description']) <= 512:
                    pass
                else:
                    messagecorrect = False
        else:
            messagecorrect = False

    #文件消息
    elif msgtype == 'file':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if 'file' in kwargs and kwargs['file']:
            if 'media_id' in kwargs['file'] and kwargs['file']['media_id']:
                pass
            else:
                messagecorrect = False
        else:
            messagecorrect = False

    #文本卡片消息
    elif msgtype == 'textcard':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if 'textcard' in kwargs and kwargs['textcard']:
            if 'title' in kwargs['textcard'] and kwargs['textcard']['title']:
                if len(kwargs['textcard']['title']) <= 128:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

            if 'description' in kwargs['textcard'] and kwargs['textcard']['description']:
                if len(kwargs['textcard']['description']) <= 512:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

            if 'url' in kwargs['textcard'] and kwargs['textcard']['url']:
                pass
            else:
                messagecorrect = False


            if 'btntxt' in kwargs['textcard'] and kwargs['textcard']['btntxt']:
                if len(kwargs['textcard']['btntxt']) <= 3*4:
                    pass
                else:
                    messagecorrect = False

        else:
            messagecorrect = False

    #图文消息
    elif msgtype == 'news':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if messagecorrect == False:
            pass
        else:
            if 'articles' in kwargs and kwargs['articles']:
                if len(kwargs['articles']) <= 8:
                    messagecorrect = messagearticles(msgtype, kwargs['articles'])
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

    # mpnews图文消息
    elif msgtype == 'mpnews':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if messagecorrect == False:
            pass
        else:
            if 'articles' in kwargs and kwargs['articles']:
                if len(kwargs['articles']) <= 8:
                    messagecorrect = messagearticles(msgtype, kwargs['articles'])
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

    # markdown消息
    elif msgtype == 'markdown':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        elif chatid != None:
            pass
        else:
            messagecorrect = False

        if 'markdown' in kwargs and kwargs['markdown']:
            if 'content' in kwargs['markdown'] and kwargs['markdown']['content']:
                if len(kwargs['markdown']['content']) <= 2048:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False
        else:
            messagecorrect = False

    #小程序通知消息
    elif msgtype == 'miniprogram_notice':
        if 'miniprogram_notice' in kwargs and kwargs['miniprogram_notice']:
            if 'appid' in kwargs['miniprogram_notice'] and kwargs['miniprogram_notice']['appid']:
                pass
            else:
                messagecorrect = False

            if 'title' in kwargs['miniprogram_notice'] and kwargs['miniprogram_notice']['title']:
                if len(kwargs['miniprogram_notice']['title']) >= 12 and\
                    len(kwargs['miniprogram_notice']['title']) <= 36:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

            if 'description' in kwargs['miniprogram_notice'] and kwargs['miniprogram_notice']['description']:
                if len(kwargs['miniprogram_notice']['description']) >= 12 and\
                    len(kwargs['miniprogram_notice']['description']) <= 36:
                    pass
                else:
                    messagecorrect = False

            if messagecorrect == False:
                pass
            else:
                if 'content_item' in kwargs['miniprogram_notice'] and kwargs['miniprogram_notice']['content_item']:
                    if len(kwargs['miniprogram_notice']['content_item']) <= 10:
                        messagecorrect = message_content_item(kwargs['miniprogram_notice']['content_item'])
                    else:
                        messagecorrect = False
        else:
            messagecorrect = False

    #任务卡片消息
    elif msgtype == 'taskcard':
        if 'agentid' in kwargs and kwargs['agentid']:
            pass
        else:
            messagecorrect = False

        if 'taskcard' in kwargs and kwargs['taskcard']:
            if 'title' in kwargs['taskcard'] and kwargs['taskcard']['title']:
                if len(kwargs['taskcard']['title']) <= 128:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

            if 'description' in kwargs['taskcard'] and kwargs['taskcard']['description']:
                if len(kwargs['taskcard']['description']) <= 512:
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

            if 'url' in kwargs['taskcard'] and kwargs['taskcard']['url']:
                if kwargs['taskcard']['url'].startswith('http') or\
                    kwargs['taskcard']['url'].startswith('https'):
                    pass
                else:
                    messagecorrect = False

                if len(kwargs['taskcard']['url']) <= 2048:
                    pass
                else:
                    messagecorrect = False

            if 'task_id' in kwargs['taskcard'] and kwargs['taskcard']['task_id']:
                if re.match(r'^[\w@-_]{1,128}$', kwargs['taskcard']['task_id']):
                    pass
                else:
                    messagecorrect = False
            else:
                messagecorrect = False

            if messagecorrect == False:
                pass
            else:
                if 'btn' in kwargs['taskcard'] and kwargs['taskcard']['btn']:
                    if len(kwargs['taskcard']['btn']) <= 2:
                        messagecorrect = message_btn(kwargs['taskcard']['btn'])
                    else:
                        messagecorrect = False
                else:
                    messagecorrect = False
        else:
            messagecorrect = False

    else:
        messagecorrect = False

    return messagecorrect

def messagearticles(msgytpe, articles):
    """

    :param msgytpe: 消息类型
    :param articles: 图文消息，一个图文消息支持1到8条图文
    :return: articles内参数正确返回True，参数错误返回False到 messagelist
    """
    # 图文消息

    messagearticles_correct = True

    if msgytpe == 'news':
        for article in articles:
            if 'title' in article and article['title']:
                if len(article['title']) <= 128:
                    pass
                else:
                    messagearticles_correct = False
            else:
                messagearticles_correct = False

            if 'url' in article and article['url']:
                pass
            else:
                messagearticles_correct = False

            if 'description' in article and article['description']:
                if len(article['description']) <= 512:
                    pass
                else:
                    messagearticles_correct = False

    # mpnews图文消息
    if msgytpe == 'mpnews':
        for article in articles:
            if 'title' in article and article['title']:
                if len(article['title']) <= 128:
                    pass
                else:
                    messagearticles_correct = False
            else:
                messagearticles_correct = False

            if 'thumb_media_id' in article and article['thumb_meida_id']:
                pass
            else:
                messagearticles_correct = False

            if 'author' in article and article['author']:
                if len(article['author']) <= 64:
                    pass
                else:
                    messagearticles_correct = False

            if 'content' in article and article['content']:
                if len(article['content']) <= 666000:
                    pass
                else:
                    messagearticles_correct = False
            else:
                messagearticles_correct = False

            if 'digest' in article and article['digest']:
                if len(article['digest']) <= 512:
                    pass
                else:
                    messagearticles_correct = False

    return messagearticles_correct

def message_content_item(content_item):
    """

    :param content_item: 消息内容键值对，最多允许10个item
    :return: content_item内参数正确返回True，参数错误返回False到 messagelist
    """
    message_content_item_correct = True

    for item in content_item:
        if 'key' in item and item['key']:
            if len(item['key']) <= 3*10:
                pass
            else:
                message_content_item_correct = False
        else:
            message_content_item_correct = False

        if 'value' in item and item['value']:
            if len(item['value']) <= 3*30:
                pass
            else:
                message_content_item_correct = False
        else:
            message_content_item_correct = False

    return message_content_item_correct

def message_btn(btns):
    """

    :param btns: 按钮列表，按钮个数为1~2个
    :return: btn内参数正确返回True，参数错误返回False到 messagelist
    """
    message_btn_correct = True

    for btn in btns:
        if 'key' in btn and btn['key']:
            if re.match(r'^[\w@-_]{1,128}$', btn['key']):
                pass
            else:
                message_btn_correct = False
        else:
            message_btn_correct = False

        if 'name' in btn and btn['name']:
            pass
        else:
            message_btn_correct = False

        if 'color' in btn and btn['color']:
            if btn['color'] == 'red' or btn['color'] == 'blue':
                pass
            else:
                message_btn_correct = False


    return message_btn_correct








