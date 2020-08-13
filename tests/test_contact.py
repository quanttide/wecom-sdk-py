
import unittest
import sys
sys.path.append("/home/john/GitHub/wechatwork-sdk-py")
# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from wechatwork_sdk.base import WeChatWorkSDK
from wechatwork_sdk.contact import UserSDK,DepartmentSDK,DepartmentTagSDK
from _config import CORPID,upload, CONTACT_SECRET,userid,create_userid,create_name,create_department,create_email,dp_name,dp_name_en,parentid,dp_id,query_params,openid


class WeChatWorkSDKUserSDK(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.wechatwork_sdk = WeChatWorkSDK(CORPID, CONTACT_SECRET)
        cls.access_token = cls.wechatwork_sdk.access_token
        cls.userskd = UserSDK(CORPID, CONTACT_SECRET)

    # 将需要的数据储存到_config中，在tag部分用到
    def test_valuable(self):
        return_data = self.userskd.valuable()

    # 测试获取部门成员，默认为只获取本部门
    def test_simplelist(self):
        # fetch_child:是否递归获取子部门下面的成员：1-递归获取，0-只获取本部门,此处默认为0
        return_data = self.userskd.simplelist(1)
        self.assertTrue('userlist' in return_data)

    # 测试创建成员
    def test_create(self):
        return_data= self.userskd.create(query_params)
        self.assertFalse(return_data)
        
    # 测试读取成员信息
    def test_get(self):
        return_data = self.userskd.get(create_userid)
        self.assertTrue(return_data)
    
    # 测试更新成员信息
    def test_update(self):
        return_data = self.userskd.update(query_params)
        self.assertFalse(return_data)

    # 测试删除成员
    def test_delete(self):
        return_data = self.userskd.delete('zhangsannnn')
        self.assertFalse(return_data)

    # 测试批量删除成员
    def test_batchdelete(self):
        return_data = self.userskd.batchdelete(['zhangsannn','zhangsannnn'])
        self.assertFalse(return_data)
    
    # 测试获取部门成员详情
    def test_list_(self):
        return_data = self.userskd.list_(1)
        self.assertTrue('userlist' in return_data)  

    # 测试使用userid转openid
    def test_convert_to_openid(self):
        return_data = self.userskd.convert_to_openid(userid)
        self.assertTrue(return_data)

    # 测试使用openid转userid
    def test_convert_to_userid(self):
        return_data = self.userskd.convert_to_userid(openid)
        self.assertTrue('userid' in return_data)

    # 测试开启二次验证
    def test_authsucc(self):
        return_data = self.userskd.authsucc(create_userid)
        self.assertFalse(return_data)

    # 测试邀请成员
    def test_invite(self):
        return_data = self.userskd.invite(create_userid,create_name,create_department)
        self.assertTrue('invaliduser' in return_data)
    
    # 测试获取加入二维码
    def test_get_join_qrcode(self):
        return_data = self.userskd.get_join_qrcode()
        self.assertTrue(return_data)
    
    # 测试获取企业活跃成员人数
    def test_get_active_stat(self):
        return_data = self.userskd.get_active_stat('2020-07-20')
        self.assertTrue(return_data) 


class WeChatWorkSDKDepartmentSDK(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.wechatwork_sdk = WeChatWorkSDK(CORPID, CONTACT_SECRET)
        cls.access_token = cls.wechatwork_sdk.access_token
        cls.dpsdk = DepartmentSDK(CORPID, CONTACT_SECRET)

    # 将需要的数据储存到_config中，在tag部分用到
    def test_valuable(self):
        return_data = self.dpsdk.valuable()

    # 测试创建部门
    def test_create(self):
        return_data = self.dpsdk.create(dp_name,parentid,dp_name_en,dp_id)
        self.assertTrue(return_data)
    
    # 测试更新部门信息
    def test_update(self):
        return_data = self.dpsdk.update(dp_id,name=dp_name)
        self.assertFalse(return_data)

    # 测试获取部门列表，默认为获取全部框架
    def test_Departmenlist(self):
        return_data = self.dpsdk.Departmenlist()
        self.assertTrue('department' in return_data)
    
    # 测试删除成员信息
    def test_delete(self):
        return_data = self.dpsdk.delete(3)
        self.assertFalse(return_data)
    
class WeChatWorkSDKTagSDK(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.wechatwork_sdk = WeChatWorkSDK(CORPID, CONTACT_SECRET)
        cls.access_token = cls.wechatwork_sdk.access_token
        cls.tagsdk = DepartmentTagSDK(CORPID, CONTACT_SECRET)
    
    # 测试创建标签
    def test_create(self):
        return_data = self.tagsdk.create('UI')
        self.assertTrue(return_data)
    
    # 测试更新标签信息
    def test_update(self):
        return_data = self.tagsdk.update(1,'UI')
        self.assertFalse(return_data)
    
    # 测试删除标签
    def test_delete(self):
        return_data = self.tagsdk.delete(3)
        self.assertFalse(return_data)
    
    # 测试获取标签成员信息
    def test_get(self):
        return_data = self.tagsdk.get(3)
        self.assertTrue(return_data)

    # 测试添加标签成员
    def test_addtagusers(self):
        return_data = self.tagsdk.addtagusers(1,'zhangsannnn')
        self.assertFalse(return_data)
    
    # 测试删除标签成员信息
    def test_deletetagusers(self):
        return_data = self.tagsdk.deltagusers(1,'zhangsannnn')
        if return_data is not None:
            if 'invalidparty' in return_data:
                if return_data['invalidparty'] == None:
                    return_data = None
                    self.assertFalse(return_data)
        self.assertFalse(return_data)

    # 测试获取标签列表
    def test_taglist(self):
        return_data = self.tagsdk.taglist()
        self.assertTrue('taglist' in return_data)



if __name__ == "__main__":
    unittest.main()

    