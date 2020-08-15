# -*- coding: utf-8 -*-
import unittest

from wechatwork_sdk.message import MessageSDK, AppchatSDK, LinkedcorpMessageSDK, messagelist
from ._config import CORPID, CLOCK_IN_ID, CLOCK_IN_SECRET, APPCHAT_SECRET


class MessageSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.message_sdk = MessageSDK(CORPID, CLOCK_IN_SECRET)

    # touser超出1000
    def test_touser(self):
        with self.assertRaises(AssertionError):
            self.message_sdk.sendmessage(msgtype='text', agentid=CLOCK_IN_ID, touser=1000*'LiXiaoJun|',
                                         text={'content': '打卡'})

    # safe参数不为1或0
    def test_safe(self):
        with self.assertRaises(AssertionError):
            self.message_sdk.sendmessage(msgtype='text', agentid=CLOCK_IN_ID, touser='LiXiaoJun',
                                         text={'content': '打卡'}, safe=2)

    # enable_id_trans不为1或0
    def test_enable_id_trans(self):
        with self.assertRaises(AssertionError):
            self.message_sdk.sendmessage(msgtype='text', agentid=CLOCK_IN_ID, touser='LiXiaoJun',
                                         text={'content': '打卡'}, enable_id_trans=2)

    # enable_duplicate_check不为1或0
    def test_enable_duplicate_check(self):
        with self.assertRaises(AssertionError):
            self.message_sdk.sendmessage(msgtype='text', agentid=CLOCK_IN_ID, touser='LiXiaoJun',
                                         text={'content': '打卡'}, enable_duplicate_check=2)

    # duplicate_check_interbal不为1或0
    def test_duplicate_check_interval(self):
        with self.assertRaises(AssertionError):
            self.message_sdk.sendmessage(msgtype='text', agentid=CLOCK_IN_ID, touser='LiXiaoJun',
                                         text={'content': '打卡'}, duplicate_check_interval=144000)

    # 测试是否能正常发送消息
    def test_sendmessage(self):
        self.message_sdk.sendmessage(msgtype='text', agentid=CLOCK_IN_ID, touser='LiXiaoJun', text={'content': '打卡'})

    # 测试是否能正常更新taskcard消息
    def test_update_taskcard(self):
        self.message_sdk.update_taskcard(userids=['LiXiaoJun'], agentid=CLOCK_IN_ID, task_id='taskid123',
                                         clicked_key='key111')

    # userids超过1000个
    def test_userids(self):
        with self.assertRaises(AssertionError):
            self.message_sdk.update_taskcard(userids=1001*['LiXiaoJun'], agentid=CLOCK_IN_ID, task_id='taskid123',
                                             clicked_key='key111')

    # 测试是否能正常统计消息发送
    def test_get_statistics(self):
        self.message_sdk.get_statistics(time_type=0)

class AppchatSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.appchat_sdk = AppchatSDK(CORPID, APPCHAT_SECRET)

    # 测试是够能正常创建appchat
    def test_create_appchat(self):
        self.appchat_sdk.create_appchat(name='NAME', owner='LiXiaoJun', userlist=['LiXiaoJun', 'ChenFan'],
                                        chatid='CHATID')

    # userlist个数少于2个
    def test_userlist(self):
        with self.assertRaises(AssertionError):
            self.appchat_sdk.create_appchat(name='NAME', owner='LiXiaoJun',
                                            userlist=["userid1"], chatid='CHATID')

    # 测试不添加owner是否会自动生成
    def test_owner(self):
        self.appchat_sdk.create_appchat(name='NAME', userlist=['ChenFan','LiXiaoJun'], chatid='CHATID')

    # 不输入chatid自动生成chatid
    def test_chatid(self):
        self.appchat_sdk.create_appchat(name='NAM', userlist=['ChenFan','LiXiaoJun'])

    # name超过50个utf-8字符
    def test_name(self):
        with self.assertRaises(AssertionError):
            self.appchat_sdk.create_appchat(name=50*'APPCHATNAME', owner='LiXiaoJun',
                                            userlist=['ChenFan','LiXiaoJun'], chatid='CHATID')

    # 测试是否能正常获取appchat信息
    def test_get_appchat(self):
        self.appchat_sdk.get_appchat(chatid='CHATID')

    # 测试是否能正常更新appchat信息
    def test_update_appchat(self):
        self.appchat_sdk.update_appchat(name='NAM', owner='LiXiaoJun', chatid='CHATID')

    def test_add_user_list(self):
        # add_user_list使得user_list超出上限2000
        with self.assertRaises(AssertionError):
            self.appchat_sdk.update_appchat(chatid='CHATID', add_user_list=2000*['x'])
        # userid首字符不是数字或字符
        with self.assertRaises(AssertionError):
            self.appchat_sdk.update_appchat(chatid='CHATID', add_user_list=['.x22'])
        # userid长度超过64字节
        with self.assertRaises(AssertionError):
            self.appchat_sdk.update_appchat(chatid='CHATID', add_user_list=[2000*'x'])

    # del_user_list大于等于原user_list中user个数
    def test_del_user_list(self):
        with self.assertRaises(AssertionError):
            self.appchat_sdk.update_appchat(chatid='CHATID', del_user_list=['LiXiaoJun','ChenFan'])

    # 测试是否能正常发送appchat消息
    def test_send_appchat(self):
        self.appchat_sdk.send_appchat(chatid='CHATID', msgtype='text',
                                      text={'content': "你的快递已到\n请携带工卡前往邮件中心领取"})

    # appchat的msgtype不包括miniprogram_notice消息
    def test_send_appchat_msgtype(self):
        with self.assertRaises(AssertionError):
            self.appchat_sdk.send_appchat(chatid='CHATID', msgtype='miniprogram_notice')

    # safe参数不为1或0
    def test_send_appchat_safe(self):
        with self.assertRaises(AssertionError):
            self.appchat_sdk.send_appchat(chatid='CHATID', msgtype='text', safe=2,
                                          text={'content':"你的快递已到\n请携带工卡前往邮件中心领取"})


class LinkedcorpMessageSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.linkedcorpmessage_sdk = LinkedcorpMessageSDK(CORPID, CLOCK_IN_SECRET)

    # 测试是够能正常发送linkedcorpmessage消息
    def test_linkedcorpmessage(self):
        self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', agentid=CLOCK_IN_ID, touser=['LiXiaoJun'],
                                                          text={"content": "你的快递已到，请携带工卡前往邮件中心领取。"})

    # toall参数不为1或0
    def test_toall(self):
        with self.assertRaises(AssertionError):
            self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', toall=2)

    # touser超过1000个
    def test_touser(self):
        with self.assertRaises(AssertionError):
            self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', agentid=CLOCK_IN_ID,
                                                              touser=1001*['LiXiaoJun'],
                                                              text={"content" : "你的快递已到。"})

    # safe参数不为1或0
    def test_linkedcorpmessage_safe(self):
            with self.assertRaises(AssertionError):
                self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', agentid=CLOCK_IN_ID,
                                                                  touser=['LiXiaoJun'],
                                                                  text={"content": "你的快递已到。"}, safe=2)


class MessagelistTestCase(unittest.TestCase):
    # msgtype不在11种类型选择范围内
    def test_msgtype(self):
        messagecorrect = messagelist(msgtype='test')
        self.assertFalse(messagecorrect)

    # agentid不存在
    def test_agentid(self):
        messagecorrect = messagelist(msgtype='text', agentid=None)
        self.assertFalse(messagecorrect)

    # text内容缺失
    def test_text(self):
        messagecorrect = messagelist(msgtype='text', agentid=CLOCK_IN_ID)
        self.assertFalse(messagecorrect)

    # content超过2048字节
    def test_text_content(self):
        messagecorrect = messagelist(msgtype='text', agentid=CLOCK_IN_ID, text={'content':1024*'content'})
        self.assertFalse(messagecorrect)

    # image内容缺失
    def test_image(self):
        messagecorrect = messagelist(msgtype='image', agentid=CLOCK_IN_ID, image=None)
        self.assertFalse(messagecorrect)

    # media_id内容缺失
    def test_media_id(self):
        messagecorrect = messagelist(msgtype='image', agentid=CLOCK_IN_ID, image={'media_id':None})
        self.assertFalse(messagecorrect)

    # voice参数不存在
    def test_voice(self):
        messagecorrect = messagelist(msgtype='voice', agentid=CLOCK_IN_ID)
        self.assertFalse(messagecorrect)

    # video内容缺失
    def test_video(self):
        messagecorrect = messagelist(msgtype='video', agentid=CLOCK_IN_ID, video={})
        self.assertFalse(messagecorrect)

    # video_title超过128字节
    def test_video_title(self):
        messagecorrect = messagelist(msgtype='video', agentid=CLOCK_IN_ID,
                                     video={'media_id':1, 'title':128*'title'})
        self.assertFalse(messagecorrect)

    # video_description超过512字节
    def test_video_description(self):
        messagecorrect = messagelist(msgtype='video', agentid=CLOCK_IN_ID,
                                     video={'media_id':1, 'description':512*'description'})
        self.assertFalse(messagecorrect)

    # file参数不存在
    def test_file(self):
        messagecorrect = messagelist(msgtype='file', agentid=CLOCK_IN_ID)
        self.assertFalse(messagecorrect)

    # textcard内容缺失
    def test_textcard(self):
        messagecorrect = messagelist(msgtype='textcard', agentid=CLOCK_IN_ID, textcard=None)
        self.assertFalse(messagecorrect)

    def test_textcard_title(self):
        # textcard_title超出128字节
        messagecorrect1 = messagelist(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'title':128*'领奖通知',
                                                'description':'<div class=\"gray\">2016年9月26日</div> '
                                                              '<div class=\"normal\">恭喜你抽中iPhone 7一台</div>'
                                                              '<div class=\"highlight\">请联系行政同事领取</div>',
                                                'url':'URL', 'btntxt':'更多'})
        self.assertFalse(messagecorrect1)

        # textcard_title参数不存在
        messagecorrect2 = messagelist(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'description':'<div class=\"gray\">2016年9月26日</div> '
                                                              '<div class=\"normal\">恭喜你抽中iPhone 7一台</div>'
                                                              '<div class=\"highlight\">请联系行政同事领取</div>',
                                                'url':'URL', 'btntxt':'更多'})
        self.assertFalse(messagecorrect2)

    # textcard_description超出512字节
    def test_textcard_description(self):
        messagecorrect = messagelist(msgtype='textcard', agentid=CLOCK_IN_ID,
                                     textcard={'title':'领奖通知',
                                               'description':'<div class=\"gray\">2016年9月26日</div> '
                                                             '<div class=\"normal\">恭喜你抽中iPhone 7一台</div>'
                                                             '<div class=\"highlight\">请联系行政同事领取</div>',
                                               'url':'URL', 'btntxt':'更多'})
        self.assertFalse(messagecorrect)

    # textcard_url参数不存在
    def test_textcard_url(self):
        messagecorrect = messagelist(msgtype='textcard', agentid=CLOCK_IN_ID,
                                     textcard={'title': '领奖通知',
                                               'description': '<div class=\"gray\">2016年9月26日</div> '
                                                             '<div class=\"normal\">恭喜你抽中iPhone 7一台</div>'
                                                             '<div class=\"highlight\">请联系行政同事领取</div>',
                                               'btntxt': '更多'})
        self.assertFalse(messagecorrect)

    # textcard_btntxt超过4个文字
    def test_textcard_btntxt(self):
        messagecorrect = messagelist(msgtype='textcard', agenid=CLOCK_IN_ID,
                                     textcard={'title': '领奖通知',
                                               'description': '<div class=\"gray\">2016年9月26日</div> '
                                                             '<div class=\"normal\">恭喜你抽中iPhone 7一台</div>'
                                                             '<div class=\"highlight\">请联系行政同事领取</div>',
                                               'url': 'URL', 'btntxt': '详情请见官网'})
        self.assertFalse(messagecorrect)

    # news内容缺失
    def test_news(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, news=None)
        self.assertFalse(messagecorrect)

    def test_news_articles(self):
        # news_articles内容缺失
        messagecorrect1 = messagelist(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': None})
        self.assertFalse(messagecorrect1)

        # news_articles超出8条图文
        messagecorrect2 = messagelist(msgtype='news', agentid=CLOCK_IN_ID,
                                      news={'articles': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]})
        self.assertFalse(messagecorrect2)

    def test_news_articles_title(self):
        # news_articles_title超出128字节
        messagecorrect1 = messagelist(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': {
               "title": 128*"中秋节礼品领取",
               "description": "今年中秋节公司有豪礼相送",
               "url": "URL",
               "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }})
        self.assertFalse(messagecorrect1)

        # news_articles_title参数不存在
        messagecorrect2 = messagelist(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': {
               "description": "今年中秋节公司有豪礼相送",
               "url": "URL",
               "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }})
        self.assertFalse(messagecorrect2)

    # news_articles_description超出512个字节
    def test_news_articles_description(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': {
               "title": "中秋节礼品领取",
               "description": 521*"今年中秋节公司有豪礼相送",
               "url": "URL",
               "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }})
        self.assertFalse(messagecorrect)

    # news_articles_url内容缺失
    def test_news_articles_url(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': {
               "title": "中秋节礼品领取",
               "description": "今年中秋节公司有豪礼相送",
               "url": None,
               "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }})
        self.assertFalse(messagecorrect)

    # mpnews内容缺失
    def test_mpnews(self):
        messagecorrect = messagelist(msgtype='mpnews', agentid=CLOCK_IN_ID, mpnews=None)
        self.assertFalse(messagecorrect)

    def test_mpnews_articles(self):
        # mpnews_articles内容缺失
        messagecorrect1 = messagelist(msgtype='mpnews', agentid=CLOCK_IN_ID, mpnews={'articles': None})
        self.assertFalse(messagecorrect1)

        # mpnews_articles超过8条图文
        messagecorrect2 = messagelist(msgtype='mpnews', agentid=CLOCK_IN_ID,
                                      mpnews={'articles': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]})
        self.assertFalse(messagecorrect2)

    # mpnews_articles_thumb_media_id参数不存在
    def test_mpnews_articles_thumb_media_id(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': {
            "title": "Title",
            "author": "Author",
            "content_source_url": "URL",
            "content": "Content",
            "digest": "Digest description"
           }})
        self.assertFalse(messagecorrect)

    # mpnews_articles_author超出64个字节
    def test_mpnews_articles_author(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': {
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": 64*"Author",
            "content_source_url": "URL",
            "content": "Content",
            "digest": "Digest description"
           }})
        self.assertFalse(messagecorrect)

    # mpnews_articles_content超过666k个字节
    def test_mpnews_articles_content(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': {
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": "Author",
            "content_source_url": "URL",
            "content": 666000*"Content",
            "digest": "Digest description"
        }})
        self.assertFalse(messagecorrect)

    # mpnews_articles_digest超过512字节
    def test_mpnews_articles_digest(self):
        messagecorrect = messagelist(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': {
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": "Author",
            "content_source_url": "URL",
            "content": "Content",
            "digest": 512*"Digest description"
        }})
        self.assertFalse(messagecorrect)

    # markdown参数不存在
    def test_markdown(self):
        messagecorrect = messagelist(msgtype='markdown', agentid=CLOCK_IN_ID)
        self.assertFalse(messagecorrect)

    # markdown_content超过2048个字节
    def test_markdown_content(self):
        messagecorrect = messagelist(msgtype='markdown', agentid=CLOCK_IN_ID,
                                     markdown={'content': 1024 *
                "您的会议室已经预定，稍后会同步到`邮箱` \
                >**事项详情** \
                >事　项：<font color=\"info\">开会</font> \
                >组织者：@miglioguan \
                >参与者：@miglioguan、@kunliu、@jamdeezhou、@kanexiong、@kisonwang \
                > \
                >会议室：<font color=\"info\">广州TIT 1楼 301</font> \
                >日　期：<font color=\"warning\">2018年5月18日</font> \
                >时　间：<font color=\"comment\">上午9:00-11:00</font> \
                > \
                >请准时参加会议。 \
                > \
                >如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)"})
        self.assertFalse(messagecorrect)

    # miniprogram_notice参数不存在
    def test_miniprogram_notice(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice')
        self.assertFalse(messagecorrect)

    # miniprogram_notice_appid参数不存在
    def test_miniprogram_notice_appid(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice', miniprogram_notice={
                "appid": None,
                "page": "pages/index?userid=zhangsan&orderid=123123123",
                "title": "会议室预订成功通知",
                "description": "4月27日 16:16",
                "emphasis_first_item": True,
                "content_item": [
                    {
                        "key": "会议室",
                        "value": "402"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    # miniprogram_notice_title超过12个汉字
    def test_miniprogram_notice_title(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice', miniprogram_notice={
                "appid": "wx123123123123123",
                "page": "pages/index?userid=zhangsan&orderid=123123123",
                "title": "会议室预订成功通知-小程序消息",
                "description": "4月27日 16:16",
                "emphasis_first_item": True,
                "content_item": [
                    {
                        "key": "会议室",
                        "value": "402"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    # miniprogram_notice_description超过12个汉字
    def test_miniprogram_notice_description(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice', miniprogram_notice={
                "appid": "wx123123123123123",
                "page": "pages/index?userid=zhangsan&orderid=123123123",
                "title": "会议室预订成功通知",
                "description": "公元2020年 4月27日-5月27日 16:16（超过12个汉字（36个字节））",
                "emphasis_first_item": True,
                "content_item": [
                    {
                        "key": "会议室",
                        "value": "402"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    # content_item个数超过10个
    def test_content_item(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice', miniprogram_notice={
                "appid": "wx123123123123123",
                "page": "pages/index?userid=zhangsan&orderid=123123123",
                "title": "会议室预订成功通知",
                "description": "公元2020年",
                "emphasis_first_item": None,
                "content_item": [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
        })
        self.assertFalse(messagecorrect)

    # content_item_key超过10个字节
    def test_content_item_key(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice', miniprogram_notice={
                "appid": "wx123123123123123",
                "page": "pages/index?userid=zhangsan&orderid=123123123",
                "title": "会议室预订成功通知",
                "description": "公元2020年",
                "emphasis_first_item": None,
                "content_item": [
                    {
                        "key": 10*"会议室",
                        "value": "402"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    # content_item_value超过30个字节
    def test_content_item_value(self):
        messagecorrect = messagelist(msgtype='miniprogram_notice', miniprogram_notice={
                "appid": "wx123123123123123",
                "page": "pages/index?userid=zhangsan&orderid=123123123",
                "title": "会议室预订成功通知",
                "description": "公元2020年",
                "emphasis_first_item": None,
                "content_item": [
                    {
                        "key": "会议室",
                        "value": 30*"402"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    # taskcard参数不存在
    def test_taskcard(self):
        messagecorrect = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID)
        self.assertFalse(messagecorrect)

    def test_taskcard_title(self):
        # taskcard_title参数不存在
        messagecorrect1 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect1)

        # taskcard_title超过128个字节
        messagecorrect2 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": 128*"赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect2)

    def test_taskcard_description(self):
        # taskcard_description参数不存在
        messagecorrect1 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect1)

        # taskcard_description超出512字节
        messagecorrect2 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": 521*"礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect2)

    def test_taskcard_url(self):
        # url超出2048个字节
        messagecorrect1 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": 1024*"https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect1)

        # url不以http/https开头
        messagecorrect2 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "URL",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect2)

    def test_taskcard_task_id(self):
        # task_id超出128字节
        messagecorrect1 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": 128*"taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect1)

        # task_id含有除字母数字@_-外的特殊字符
        messagecorrect2 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123,",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准",
                    }
                ]
        })
        self.assertFalse(messagecorrect2)

    # btn个数超过2个
    def test_taskcard_btn(self):
        messagecorrect = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": 128 * "taskid123",
                "btn": [
                    {
                        "key": "key111",
                        "name": "批准",
                    },
                    {
                        "key": "key222",
                        "name": "驳回",
                        "replace_name": "已驳回"
                    },
                    {
                        "key": "key222",
                        "name": "驳回",
                        "replace_name": "已驳回"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    def test_taskcard_btn_key(self):
        # btn:key超过128字节
        messagecorrect1 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": 128*"key111",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect1)

        # btn:key含有非法字符
        messagecorrect2 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key111。",
                        "name": "批准"
                    }
                ]
        })
        self.assertFalse(messagecorrect2)

        # btn:key不存在
        messagecorrect3 = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "name": "批准",
                    }
                ]
        })
        self.assertFalse(messagecorrect3)

    # btn:name不存在
    def test_taskcard_btn_name(self):
        messagecorrect = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key222"
                    }
                ]
        })
        self.assertFalse(messagecorrect)

    # btn:color不为red或者blue
    def test_taskcard_btn_color(self):
        messagecorrect = messagelist(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
                "title": "赵明登的礼物申请",
                "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
                "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
                "task_id": "taskid123",
                "btn": [
                    {
                        "key": "key222",
                        "name": "批准",
                        "replace_name": "已批准",
                        "color": "yellow"
                    }
                ]
        })
        self.assertFalse(messagecorrect)


if __name__ == '__main__':
    unittest.main()
