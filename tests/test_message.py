# -*- coding: utf-8 -*-
import unittest
from wechatwork_sdk.message import MessageSDK, AppchatSDK, LinkedcorpMessageSDK, TextMessage, ImageMessage, \
                                    VoiceMessage, VideoMessage, FileMessage, TextcardMessage, NewsMessage, \
                                    MpnewsMessage, MarkdownMessage, MiniprogramnoticeMessage,TaskcardMessage
from ._config import CORPID, CLOCK_IN_ID, CLOCK_IN_SECRET, APPCHAT_SECRET


class MessageSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.message_sdk = MessageSDK(CORPID, CLOCK_IN_SECRET)

    # 测试是否能正常发送消息
    def test_send_message(self):
        self.message_sdk.send_message(msgtype='text', agentid=CLOCK_IN_ID, touser='LiXiaoJun', text={'content': '打卡'})

    # touser超出1000
    def test_touser(self):
        err_message = self.message_sdk.send_message(msgtype='text', agentid=CLOCK_IN_ID, touser=1000*'LiXiaoJun|',
                                                    text={'content': '打卡'})
        self.assertIn('touser、toparty、totag参数错误', err_message)

    # msgtype不在11种类型选择范围内
    def test_msgtype(self):
        err_message = self.message_sdk.send_message(msgtype='test', agentid=CLOCK_IN_ID, touser='LiXiaoJun',
                                                    text={'content': '打卡'})
        self.assertIn('msgtype参数错误', err_message)

    # 测试是否能正常更新taskcard消息
    def test_update_taskcard(self):
        self.message_sdk.update_taskcard(userids=['LiXiaoJun'], agentid=CLOCK_IN_ID, task_id='taskid123',
                                         clicked_key='key111')

    # 缺少agentid
    def test_update_taskcard_agentid(self):
        err_message = self.message_sdk.update_taskcard(userids=['LiXiaoJun'], task_id='taskid123', clicked_key='key111')
        self.assertIn('缺少agentid参数', err_message)

    # userids超过1000个
    def test_userids(self):
        err_message = self.message_sdk.update_taskcard(userids=1001*['LiXiaoJun'], agentid=CLOCK_IN_ID, task_id='taskid123',
                                                       clicked_key='key111')
        self.assertIn('userids参数错误', err_message)

    # 测试是否能正常统计消息发送
    def test_get_statistics(self):
        self.message_sdk.get_statistics(time_type=0)


class AppchatSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.appchat_sdk = AppchatSDK(CORPID, APPCHAT_SECRET)

    # 测试是够能正常创建appchat
    def _create_appchat(self):
        self.appchat_sdk.create_appchat(name='NAME', owner='LiXiaoJun', userlist=['LiXiaoJun', 'ChenFan'],
                                        chatid='ID')

    # userlist个数少于2个
    def test_userlist(self):
        err_message = self.appchat_sdk.create_appchat(name='NAME', owner='LiXiaoJun', userlist=["userid1"], chatid='ID')
        self.assertIn('userlist参数错误', err_message)

    # 测试不添加owner是否会自动生成
    def test_owner(self):
        self.appchat_sdk.create_appchat(name='NAME', userlist=['ChenFan', 'LiXiaoJun'], chatid='CH')

    # 不输入chatid自动生成chatid
    def test_chatid(self):
        self.appchat_sdk.create_appchat(name='NAM', userlist=['ChenFan', 'LiXiaoJun'])

    # name超过50个utf-8字符
    def test_name(self):
        err_message = self.appchat_sdk.create_appchat(name=50*'APPCHATNAME', owner='LiXiaoJun',
                                                      userlist=['ChenFan', 'LiXiaoJun'], chatid='CHATID')
        self.assertIn('name参数错误', err_message)

    # 测试是否能正常获取appchat信息
    def test_get_appchat(self):
        self.appchat_sdk.get_appchat(chatid='CHATID')

    # 测试是否能正常更新appchat信息
    def test_update_appchat(self):
        self.appchat_sdk.update_appchat(name='NAM', owner='LiXiaoJun', chatid='CHATID')

    def test_add_user_list(self):
        # add_user_list使得user_list超出上限2000
        err_message = self.appchat_sdk.update_appchat(chatid='CHATID', add_user_list=2000*['x'])
        self.assertIn('add_user_list参数错误', err_message)

        # userid首字符不是数字或字符
        err_message = self.appchat_sdk.update_appchat(chatid='CHATID', add_user_list=['.x22'])
        self.assertIn('add_user_list参数错误', err_message)

        # userid长度超过64字节
        err_message = self.appchat_sdk.update_appchat(chatid='CHATID', add_user_list=[2000*'x'])
        self.assertIn('add_user_list参数错误', err_message)

    # del_user_list大于等于原user_list中user个数
    def test_del_user_list(self):
        err_message = self.appchat_sdk.update_appchat(chatid='CHATID',
                                                      del_user_list=['LiXiaoJun', 'ChenFan', 'ZhangGuo'])
        self.assertIn('del_user_list参数错误', err_message)

    # 测试是否能正常发送appchat消息
    def test_send_appchat(self):
        self.appchat_sdk.send_appchat(chatid='CHATID', msgtype='text',
                                      text={'content': "你的快递已到\n请携带工卡前往邮件中心领取"})

    # appchat的msgtype不包括miniprogram_notice消息
    def test_send_appchat_msgtype(self):
        err_message = self.appchat_sdk.send_appchat(chatid='CHATID', msgtype='miniprogram_notice')
        self.assertIn('msgtype参数错误', err_message)

    # safe参数不为1或0
    def test_send_appchat_safe(self):
        err_message = self.appchat_sdk.send_appchat(chatid='CHATID', msgtype='text', safe=2,
                                                    text={'content': "你的快递已到\n请携带工卡前往邮件中心领取"})
        self.assertIn('safe参数错误', err_message)


class LinkedcorpMessageSDKTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.linkedcorpmessage_sdk = LinkedcorpMessageSDK(CORPID, CLOCK_IN_SECRET)

    # 测试是够能正常发送linkedcorpmessage消息
    def test_linkedcorpmessage(self):
        self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', agentid=CLOCK_IN_ID, touser=['LiXiaoJun'],
                                                          text={"content": "你的快递已到。"})

    # toall参数不为1或0
    def test_toall(self):
        err_message = self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', toall=2)
        self.assertIn('touser、toparty、totag参数错误', err_message)

    # touser超过1000个
    def test_touser(self):
        err_message = self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', agentid=CLOCK_IN_ID,
                                                                        touser=1001*['LiXiaoJun'],
                                                                        text={"content": "你的快递已到。"})
        self.assertIn('touser、toparty、totag参数错误', err_message)

    # safe参数不为1或0
    def test_linkedcorpmessage_safe(self):
        err_message = self.linkedcorpmessage_sdk.send_linkedcorpmessage(msgtype='text', agentid=CLOCK_IN_ID,
                                                                        touser=['LiXiaoJun'],
                                                                        text={"content": "你的快递已到。"}, safe=2)
        self.assertIn('safe参数错误', err_message)


class TextMessageTestCase(unittest.TestCase):
    # agentid、chatid不存在
    def test_agentid(self):
        err_message = TextMessage(msgtype='text', agentid=None).text_err()
        self.assertIn('agentid或chatid不存在', err_message)

    # content内容缺失
    def test_text(self):
        err_message = TextMessage(msgtype='text', agentid=CLOCK_IN_ID).text_err()
        self.assertIn('content参数错误', err_message)

    # content超过2048字节
    def test_text_content(self):
        err_message = TextMessage(msgtype='text', agentid=CLOCK_IN_ID, text={'content': 1024 * 'content'}).text_err()
        self.assertIn('content参数错误', err_message)

    # safe不为0或1
    def test_safe(self):
        err_message = TextMessage(msgtype='text', agentid=CLOCK_IN_ID, text={'content': 'content'}, safe=2).text_err()
        self.assertIn('safe参数错误', err_message)

    # enable_id_trans不为0或1
    def test_enable_id_trans(self):
        err_message = TextMessage(msgtype='text', agentid=CLOCK_IN_ID, text={'content': 'content'},
                                  enable_id_trans=2).text_err()
        self.assertIn('enable_id_trans参数错误', err_message)

    # enable_duplicate_check不为0或1
    def test_enable_duplicate_check(self):
        err_message = TextMessage(msgtype='text', agentid=CLOCK_IN_ID, text={'content': 'content'},
                                  enable_duplicate_check=2).text_err()
        self.assertIn('enable_duplicate_check参数错误', err_message)

    # duplicate_check_interval超过14400
    def test_duplicate_check_interval(self):
        err_message = TextMessage(msgtype='text', agentid=CLOCK_IN_ID, text={'content': 'content'},
                                  duplicate_check_interval=20000).text_err()
        self.assertIn('duplicate_check_interval参数错误', err_message)


class ImageMessageTestCase(unittest.TestCase):
    # media_id不存在
    def test_image_media_id(self):
        err_message = ImageMessage(msgtype='image', agentid=CLOCK_IN_ID, image={'media_id': None}).image_err()
        self.assertIn('media_id参数错误', err_message)


class VoiceMessageTestCase(unittest.TestCase):
    # media_id不存在
    def test_voice_media_id(self):
        err_message = VoiceMessage(msgtype='voice', agentid=CLOCK_IN_ID, voice={'media_id': None}).voice_err()
        self.assertIn('media_id参数错误', err_message)


class VideoMessageTestCase(unittest.TestCase):
    # video不存在
    def test_video(self):
        err_message = VideoMessage(msgtype='video', agentid=CLOCK_IN_ID).video_err()
        self.assertIn('缺少video参数', err_message)

    # media_id不存在
    def test_video_media_id(self):
        err_message = VideoMessage(msgtype='video', agentid=CLOCK_IN_ID, video={'media_id': None}).video_err()
        self.assertIn('media_id参数错误', err_message)

    # video_title超过128字节
    def test_video_title(self):
        err_message = VideoMessage(msgtype='video', agentid=CLOCK_IN_ID,
                                   video={'media_id': 1, 'title': 128*'title'}).video_err()
        self.assertIn('title参数错误', err_message)

    # video_description超过512字节
    def test_video_description(self):
        err_message = VideoMessage(msgtype='video', agentid=CLOCK_IN_ID,
                                   video={'media_id': 1, 'description': 512*'description'}).video_err()
        self.assertIn('description参数错误', err_message)


class FileMessageTestCase(unittest.TestCase):
    # media_id不存在
    def test_file_media_id(self):
        err_message = FileMessage(msgtype='file', agentid=CLOCK_IN_ID, file={'media_id': None}).file_err()
        self.assertIn('media_id参数错误', err_message)


class TextcardMessageTestCase(unittest.TestCase):
    # textcard内容缺失
    def test_textcard(self):
        err_message = TextcardMessage(msgtype='textcard', agentid=CLOCK_IN_ID, textcard=None).textcard_err()
        self.assertIn('缺少textcard参数', err_message)

    def test_textcard_title(self):
        # textcard_title超出128字节
        err_message = TextcardMessage(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'title': 128 * '领奖通知',
                                                'description': '<div class=\"gray\">2016年9月26日</div> ',
                                                'url': 'URL', 'btntxt': '更多'}).textcard_err()
        self.assertIn('title参数错误', err_message)

        # textcard_title参数不存在
        err_message = TextcardMessage(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'description': '<div class=\"gray\">2016年9月26日</div> ',
                                                'url': 'URL', 'btntxt': '更多'}).textcard_err()
        self.assertIn('title参数错误', err_message)

    # textcard_description超出512字节
    def test_textcard_description(self):
        err_message = TextcardMessage(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'title': '领奖通知',
                                                'description': 512 * '<div class=\"gray\">2016年9月26日</div> ',
                                                'url': 'URL', 'btntxt': '更多'}).textcard_err()
        self.assertIn('description参数错误', err_message)

    # textcard_url参数不存在
    def test_textcard_url(self):
        err_message = TextcardMessage(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'title': '领奖通知',
                                                'description': '<div class=\"gray\">2016年9月26日</div> ',
                                                'btntxt': '更多'}).textcard_err()
        self.assertIn('缺少url参数', err_message)

    # textcard_btntxt超过4个文字
    def test_textcard_btntxt(self):
        err_message = TextcardMessage(msgtype='textcard', agentid=CLOCK_IN_ID,
                                      textcard={'title': '领奖通知', 'description': '<div class=\"gray\">2016年9月26日</div> ',
                                                'url': 'URL', 'btntxt': '详情请见官网介绍'}).textcard_err()
        self.assertIn('btntxt参数错误', err_message)


class NewsMessageTestCase(unittest.TestCase):
    def test_news_articles(self):
        # news_articles内容缺失
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': None}).news_err()
        self.assertIn('articles参数错误', err_message)

        # news_articles超出8条图文
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID,
                                  news={'articles': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]}).news_err()
        self.assertIn('articles参数错误', err_message)

    def test_news_articles_title(self):
        # news_articles_title超出128字节
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': [{
            "title": 128 * "中秋节礼品领取",
            "description": "今年中秋节公司有豪礼相送",
            "url": "URL",
            "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        }]}).news_err()
        self.assertIn('title参数错误', err_message)

        # news_articles_title参数不存在
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': [{
            "description": "今年中秋节公司有豪礼相送",
            "url": "URL",
            "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        }]}).news_err()
        self.assertIn('title参数错误', err_message)

    # news_articles_description超出512个字节
    def test_news_articles_description(self):
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': [{
            "title": "中秋节礼品领取",
            "description": 521 * "今年中秋节公司有豪礼相送",
            "url": "URL",
            "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        }]}).news_err()
        self.assertIn('description参数错误', err_message)

    # news_articles_url内容缺失
    def test_news_articles_url(self):
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': [{
            "title": "中秋节礼品领取",
            "description": "今年中秋节公司有豪礼相送",
            "url": None,
            "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        }]}).news_err()
        self.assertIn('url参数错误', err_message)

    # piurl内容缺失
    def test_news_piurl(self):
        err_message = NewsMessage(msgtype='news', agentid=CLOCK_IN_ID, news={'articles': [{
            "title": "中秋节礼品领取",
            "description": "今年中秋节公司有豪礼相送",
            "url": None,
            "picurl": None
        }]}).news_err()
        self.assertIn('picurl参数错误', err_message)


class MpnewsMessageTestCase(unittest.TestCase):
    # mpnews内容缺失
    def test_mpnews(self):
        err_message = MpnewsMessage(msgtype='mpnews', agentid=CLOCK_IN_ID, mpnews=None).mpnews_err()
        self.assertIn('articles参数错误', err_message)

    def test_mpnews_articles(self):
        # mpnews_articles内容缺失
        err_message = MpnewsMessage(msgtype='mpnews', agentid=CLOCK_IN_ID, mpnews={'articles': None}).mpnews_err()
        self.assertIn('articles参数错误', err_message)

        # mpnews_articles超过8条图文
        err_message = MpnewsMessage(msgtype='mpnews', agentid=CLOCK_IN_ID,
                      mpnews={'articles': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]}).mpnews_err()
        self.assertIn('articles参数错误', err_message)

    # mpnews_articles_thumb_media_id参数不存在
    def test_mpnews_articles_thumb_media_id(self):
        err_message = MpnewsMessage(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': [{
            "title": "Title",
            "author": "Author",
            "content_source_url": "URL",
            "content": "Content",
            "digest": "Digest description"
        }]}).mpnews_err()
        self.assertIn('缺少thumb_media_id参数', err_message)

    # mpnews_articles_author超出64个字节
    def test_mpnews_articles_author(self):
        err_message = MpnewsMessage(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': [{
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": 64 * "Author",
            "content_source_url": "URL",
            "content": "Content",
            "digest": "Digest description"
        }]}).mpnews_err()
        self.assertIn('author参数错误', err_message)

    # mpnews_articles_content超过666k个字节
    def test_mpnews_articles_content(self):
        err_message = MpnewsMessage(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': [{
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": "Author",
            "content_source_url": "URL",
            "content": 666000 * "Content",
            "digest": "Digest description"
        }]}).mpnews_err()
        self.assertIn('content参数错误', err_message)

    # mpnews_articles_digest超过512字节
    def test_mpnews_articles_digest(self):
        err_message = MpnewsMessage(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': [{
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": "Author",
            "content_source_url": "URL",
            "content": "Content",
            "digest": 512 * "Digest description"
        }]}).mpnews_err()
        self.assertIn('digest参数错误', err_message)

    # mpnews_articles_content_source_url内容缺失
    def test_mpnews_articles_content_source_url(self):
        err_message = MpnewsMessage(msgtype='news', agentid=CLOCK_IN_ID, mpnews={'articles': [{
            "title": "Title",
            "thumb_media_id": "MEDIA_ID",
            "author": "Author",
            "content_source_url": None,
            "content": "Content",
            "digest": "Digest description"
        }]}).mpnews_err()
        self.assertIn('content_source_url参数错误', err_message)


class MarkdownMessageTestCase(unittest.TestCase):
    # markdown参数不存在
    def test_markdown(self):
        err_message = MarkdownMessage(msgtype='markdown', agentid=CLOCK_IN_ID).markdown_err()
        self.assertIn('content参数错误', err_message)

    # markdown_content超过2048个字节
    def test_markdown_content(self):
        err_message = MarkdownMessage(msgtype='markdown', agentid=CLOCK_IN_ID,
                        markdown={'content': 1024 *
                                  "您的会议室已经预定，稍后会同步到`邮箱` \
                                  >事　项：<font color=\"info\">开会</font> \
                                  >组织者：@miglioguan \
                                  >会议室：<font color=\"info\">广州TIT 1楼 301</font> \
                                  >日　期：<font color=\"warning\">2018年5月18日</font> \
                                  >时　间：<font color=\"comment\">上午9:00-11:00</font> \
                                  >如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)"}).markdown_err()
        self.assertIn('content参数错误', err_message)


class MiniprogramnoticeMessageTestCase(unittest.TestCase):
    # miniprogram_notice参数不存在
    def test_miniprogram_notice(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice').miniprogramnotice_err()
        self.assertIn('miniprogram参数错误', err_message)

    # miniprogram_notice_appid参数不存在
    def test_miniprogram_notice_appid(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
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
        }).miniprogramnotice_err()
        self.assertIn('appid参数错误', err_message)

    # miniprogram_notice_title超过12个汉字
    def test_miniprogram_notice_title(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
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
            ]}).miniprogramnotice_err()
        self.assertIn('title参数错误', err_message)

    # miniprogram_notice_page超过12个汉字
    def test_miniprogram_notice_page(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
            "appid": "wx123123123123123",
            "page": None,
            "title": "会议室预订成功通知",
            "description": "公元2020年",
            "emphasis_first_item": True,
            "content_item": [
                {
                    "key": "会议室",
                    "value": "402"
                }
            ]
        }).miniprogramnotice_err()
        self.assertIn('page参数错误', err_message)

    # miniprogram_notice_description超过12个汉字
    def test_miniprogram_notice_description(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
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
        }).miniprogramnotice_err()
        self.assertIn('description参数错误', err_message)

    # content_item无内容
    def test_content_item(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
            "appid": "wx123123123123123",
            "page": "pages/index?userid=zhangsan&orderid=123123123",
            "title": "会议室预订成功通知",
            "description": "公元2020年",
            "emphasis_first_item": None,
            "content_item": None
        }).miniprogramnotice_err()
        self.assertIn('content_item参数错误', err_message)

    # content_item_key超过10个汉字
    def test_content_item_key(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
            "appid": "wx123123123123123",
            "page": "pages/index?userid=zhangsan&orderid=123123123",
            "title": "会议室预订成功通知",
            "description": "公元2020年",
            "emphasis_first_item": None,
            "content_item": [
                {
                    "key": 10 * "会议室",
                    "value": "402"
                }
            ]
        }).miniprogramnotice_err()
        self.assertIn('key参数错误', err_message)

    # content_item_value超过30个汉字
    def test_content_item_value(self):
        err_message = MiniprogramnoticeMessage(msgtype='miniprogram_notice', miniprogram_notice={
            "appid": "wx123123123123123",
            "page": "pages/index?userid=zhangsan&orderid=123123123",
            "title": "会议室预订成功通知",
            "description": "公元2020年",
            "emphasis_first_item": None,
            "content_item": [
                {
                    "key": "会议室",
                    "value": 30 * "402室"
                }
            ]
        }).miniprogramnotice_err()
        self.assertIn('value参数错误', err_message)


class TaskcardMessageTestCase(unittest.TestCase):
    # agentid不存在
    def test_taskcard_agentid(self):
        err_message = TaskcardMessage(msgtype='taskcard').taskcard_err()
        self.assertIn('agentid参数错误', err_message)

    # taskcard参数不存在
    def test_taskcard(self):
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID).taskcard_err()
        self.assertIn('taskcard参数错误', err_message)

    def test_taskcard_title(self):
        # taskcard_title参数不存在
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('title参数错误', err_message)

        # taskcard_title超过128个字节
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": 128 * "赵明登的礼物申请",
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('title参数错误', err_message)

    def test_taskcard_description(self):
        # taskcard_description参数不存在
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('description参数错误', err_message)

        # taskcard_description超出512字节
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "description": 521 * "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('description参数错误', err_message)

    def test_taskcard_url(self):
        # url超出2048个字节
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": 1024 * "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('url参数错误', err_message)

        # url不以http/https开头
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
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
        }).taskcard_err()
        self.assertIn('url参数错误', err_message)

    def test_taskcard_task_id(self):
        # task_id超出128字节
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": 128 * "taskid123",
            "btn": [
                {
                    "key": "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('task_id参数错误', err_message)

        # task_id含有除字母数字@_-外的特殊字符
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
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
        }).taskcard_err()
        self.assertIn('task_id参数错误', err_message)

    # btn个数超过2个
    def test_taskcard_btn(self):
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
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
        }).taskcard_err()
        self.assertIn('btn参数错误', err_message)

    def test_taskcard_btn_key(self):
        # btn:key超过128字节
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": 128 * "key111",
                    "name": "批准"
                }
            ]
        }).taskcard_err()
        self.assertIn('btn:key参数错误', err_message)

        # btn:key含有非法字符
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
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
        }).taskcard_err()
        self.assertIn('btn:key参数错误', err_message)

        # btn:key不存在
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "name": "批准",
                }
            ]
        }).taskcard_err()
        self.assertIn('btn:key参数错误', err_message)

    # btn:name不存在
    def test_taskcard_btn_name(self):
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
            "title": "赵明登的礼物申请",
            "description": "礼品：A31茶具套装<br>用途：赠与小黑科技张总经理",
            "url": "https://work.weixin.qq.com/api/doc/90000/90135/90236",
            "task_id": "taskid123",
            "btn": [
                {
                    "key": "key222"
                }
            ]
        }).taskcard_err()
        self.assertIn('btn:name参数错误', err_message)

    # btn:color不为red或者blue
    def test_taskcard_btn_color(self):
        err_message = TaskcardMessage(msgtype='taskcard', agentid=CLOCK_IN_ID, taskcard={
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
        }).taskcard_err()
        self.assertIn('btn:color参数错误', err_message)


if __name__ == '__main__':
    unittest.main()
