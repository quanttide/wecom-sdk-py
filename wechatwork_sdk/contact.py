# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/john/GitHub/wechatwork-sdk-py")

from wechatwork_sdk.base import WeChatWorkSDK
from wechatwork_sdk.exception import WeChatWorkError

import datetime
import time
import json
import _config

def write_config(data):
    f = open('_config.py','a+')
    f.write(data)
    f.close()


class UserSDK(WeChatWorkSDK,WeChatWorkError):
    API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'user/'
    # checkuserid = []
    # def __init__(self):
    #     self.checkuserid = self.simplelist(1,1)

    def simplelist(self,department_id,fetch_child=0):
        """
        param department_id: 获取的部门id
        param fetch_child:是否递归获取子部门下面的成员：1-递归获取，0-只获取本部门,此处默认为0
        """

        return self.get_api(api='simplelist',query_params={'department_id':department_id,'fetch_child':fetch_child})
    # 为后续调用
    def valuable(self):
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]
        data_name = '\nuseridlist=' + str(simplelist)
        for i in range(1):
            try:
                _config.useridlist
            except:
                write_config(data)
        return
    def get(self,userid):
        """
        读取成员
        :param userid: 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节。
        :return:
        """
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]
        userid = userid.lower()

        
        # 检查是useris是否存在
        if userid in simplelist:
            return self.get_api(api='get', query_params={'userid': userid})
        else:
            print('userid not found')
            return{'error':'不存在该id'}
    def list_(self,department_id,fetch_child=0):
        """
        param department_id: 获取的部门id
        param fetch_child:是否递归获取子部门下面的成员：1-递归获取，0-只获取本部门,此处默认为0
        """
        # 获取部门成员详情，并验证部门是否存在
        partyidlist = _config.partyidlist
        if department_id in partyidlist:
            return self.get_api(api='list',query_params={'department_id':department_id,'fetch_child':fetch_child})
        else:
            return {'error':'不存在该部门'}

    def create(self,query_params):
        """
        创建成员
        :
        ：return errcode:返回码，0则正常，反之出现异常
        : return errmsg:返回码描述
        """
        # 检查mobile 和 email是否存在
        mobile = [i['mobile'] for i in self.list_(1,1)['userlist']]
        email = [i['email'] for i in self.list_(1,1)['userlist']]
        if query_params['mobile'] not in mobile:
            if query_params['email'] not in email:
                return self.post_api(api = 'create',data = query_params)
            else:
                print('email not found')
                return
        else:
            print('mobile not found')
            return
        

    def update(self,param):
        '''
        param access_token:调用接口凭证
        param userid : 成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节
        param name : 成员名称。长度为1~64个utf8字符
        param alias :别名。长度为1-32个utf8字符
        param mobile :手机号码。企业内必须唯一。若成员已激活企业微信，则需成员自行修改（此情况下该参数被忽略，但不会报错）
        param department :成员所属部门id列表，不超过100个
        param order :部门内的排序值，默认为0。数量必须和department一致，数值越大排序越前面。有效的值范围是[0, 2^32)
        param position :职务信息。长度为0~128个字符
        param gender :性别。1表示男性，2表示女性
        param email :邮箱。长度不超过64个字节，且为有效的email格式。企业内必须唯一。若是绑定了腾讯企业邮的企业微信，则需要在腾讯企业邮中修改邮箱（此情况下该参数被忽略，但不会报错）
        param telephone  :座机。由1-32位的纯数字或’-‘号组成
        param is_leader_in_dept: 上级字段，个数必须和department一致，表示在所在的部门内是 为上级。
        param avatar_mediaid  :成员头像的mediaid，通过素材管理接口上传图片获得的mediaid
        param enable :启用/禁用成员。1表示启用成员，0表示禁用成员
        param extattr  :自定义字段。自定义字段需要先在WEB管理端添加，见扩展属性添加方法， 则忽略未知属性的赋值。与对外属性一致，不过只支持type=0的文本和type=1的网页类型，详细描述查看对外属性
        param external_profile  :成员对外属性，字段详情见对外属性
        param external_position  :对外职务，如果设置了该值，则以此作为对外展示的职务， 则以position来展示。不超过12个汉字
        param address  :地址。长度最大128个字符
        param main_department : 主部门
        '''
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]

        if param['userid'] in simplelist:
            return self.post_api(api = 'update',data = param)
        else:
            print('userid not found')
            return

    def delete(self, userid):
        # param userid:成员UserID。对应管理端的帐号，企业内必须唯一。不区分大小写，长度为1~64个字节
        #删除成员，传入userid
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]
        userid = userid.lower()
        if userid in simplelist:
            return self.get_api(api='delete',query_params={"userid":userid})
        else:
            print('userid not found')
            return 

    def batchdelete(self, useridlist):
        # 最多支持同时删除200个,且如果存在无效则抛出错误
        WeChatWorkError.overlength(useridlist,200)

        # 检查是否存在，若存在则存入另一个list
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]
        userid_list = []
        for userid in useridlist:
            if userid in simplelist:
                userid_list.append(userid)

                return self.post_api(api='batchdelete',data={"useridlist":userid_list})
    
    
    def convert_to_openid(self,userid):
        # param userid:企业内的成员id
        # 验证是否存在，若不存在则返回错误信息
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]
        userid = userid.lower()
        if userid in simplelist:
            return self.post_api(api = 'convert_to_openid',data={'userid':userid})
        else:
            return {'Error':'不存在该id'}

    def convert_to_userid(self,openid):
        # param openid:企业微信成员userid对应的openid
        return self.post_api(api = 'convert_to_userid',data = {'openid':openid})
    
    def authsucc(self,userid):
        # param userid:	成员UserID。对应管理端的帐号
        # 验证是否存在，若不存在则返回错误信息
        simplelist = [i['userid'].lower() for i in self.simplelist(1,1)['userlist']]
        userid = userid.lower()
        if userid in simplelist:
            return self.get_api(api = 'authsucc',query_params = {'userid':userid})
        else:
            return

    def get_active_stat(self,date):
        # param date :需要得到指定日期的活跃 成员

        date_list = WeChatWorkError.dateRange()
        if date in date_list:
            return self.post_api(api = 'get_active_stat',data={'date':date})
        else:
            return {'error':'超出时间范围或格式不对'}

    # url发生变化，进行更改
    def invite(self,user=None,party=None,tag=None):
        """
        :param user:成员ID列表, 最多支持1000个
        :param party:部门ID列表，最多支持100个
        :param tag:标签ID列表，最多支持100个
        """
        WeChatWorkError.overlength(user,1000)
        WeChatWorkError.overlength(party,100)
        # WeChatWorkError.overlength(tag,100)

        return self.post_api(api='invite',data={'user':user,'party':party,'tag':tag})

    # url发生变化，进行更改
    # API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'corp/'
    def get_join_qrcode(self,size_type=3):
        """
        :param size_type: QRCode size:1: 171 x 171; 2: 399 x 399; 3: 741 x 741; 4: 2052 x 2052，默认设置为3
        :return 因为这里仅关注链接，因此仅返回链接
        """
        
        get_content = self.get_api(api='get_join_qrcode',query_params={'size_type':size_type})
        return get_content


class DepartmentSDK(WeChatWorkSDK):
    API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'department/'


    def Departmenlist(self,id_=None):
        # id 非必须参数，若为none则获取全量组织构架
        return self.get_api(api='list',query_params={'id':id_})

    #　将需要的信息保存到config中，并且若存在则不保存
    def valuable(self):
        all_Dep_ids = [i['id'] for i in self.Departmenlist()['department']]
        data_name = '\npartyidlist=' + str(all_Dep_ids)
        for i in range(1):
            try:
                _config.partyidlist
            except:
                write_config(data_name)
        return

    def create(self,name,parentid,name_en=None,order=None,id_=None):
        """
        # params name:部门名称，长度为1~32字符，不能包括\:?"<>/ #
        # params name_en:需要开启多语言支持,其余同上,# 
        # params parentid:父部门id,32位整型#
        # params order:在父部门中的次序,#
        # params id: 部门id,32位整型，必须大于1,若为none则自动生成
        """
        # 验证是否存在，若不存在则返回错误信息
        all_Dep_ids = [i['id'] for i in self.Departmenlist()['department']]
        if parentid not in all_Dep_ids:
            data_params = {'name':name, 'name_en':name_en,'parentid':parentid, 'order':order, 'id':id_}
            return self.post_api(api='create',data=data_params)
        else:
            # 验证是否存在，若不存在则返回错误信息
            return {'error':'该部门已经存在'}
    
    def update(self,id_,name,name_en=None,parentid=None,order=None):
        """"
        :param id_: 部门id
        :param name:部门名称，长度为1~32字符，不能包括\:?"<>/
        :param name_en:需要开启多语言支持,其余同上,# 
        :param parentid:父部门id
        :param order:在父部门中的次序,#
        """
        # 验证是否存在，若不存在则打印出，同时返回空
        all_Dep_ids = [i['id'] for i in self.Departmenlist()['department']]
        if id_ in all_Dep_ids:
            # 对长度进行处理
            WeChatWorkError.lesslength(name,1)
            WeChatWorkError.overlength(name,32)
            WeChatWorkError.lesslength(name_en,1)
            WeChatWorkError.overlength(name_en,32)

            data_params = {'id':id_,'name':name, 'name_en':name_en,'parentid':parentid,'order':order}
            return self.post_api(api='update',data=data_params)
        else:
            return 
    
    def delete(self,id_):
        # 不能删除根部门，不能删除含有子部门、成员的部门
        # 验证是否存在，若不存在则打印出，同时返回空
        all_Dep_ids = [i['id'] for i in self.Departmenlist()['department']]
        if id_ in all_Dep_ids:
            return self.get_api(api='delete',query_params={'id':id_})
        else:
            print('Departmenid not found')
            return
    
class DepartmentTagSDK(WeChatWorkSDK):
    API_ROOT_URL = WeChatWorkSDK.API_ROOT_URL + 'tag/'
    

    def taglist(self):

        return self.get_api(api='list')

    def create(self,tagname,tagid=None):
        """
        :param tagname:标签名称，长度小于32字，不可以与其他的标签重复 TODO：解决标签重复问题
        """
        # 验证是否存在，若不存在则打印出，同时返回空
        tagidlist = [i['tagid'] for i in self.taglist()['taglist']]
        tagnamelist = [i['tagname'] for i in self.taglist()['taglist']]
        if tagname not in tagnamelist:
            if tagid not in tagidlist:
                WeChatWorkError.overlength(tagname,32)
                return self.post_api(api = 'create',data={'tagname':tagname, 'tagid':tagid})
            else:
                return {'error':'该id已经存在'}
        else:
            return {'error':'该标签已经存在'}

    def update(self,tagid,tagname):
        """
        :param tagid:标签ID
        :param tagname:标签名称，长度小于32字，不可以与其他的标签重复
        """
        # 验证是否存在，若不存在则打印出，同时返回空
        tagidlist = [i['tagid'] for i in self.taglist()['taglist']]
        tagnamelist = [i['tagname'] for i in self.taglist()['taglist']]
        if tagname in tagnamelist:
            if tagid in tagidlist:
                WeChatWorkError.overlength(tagname,32)
                return self.post_api(api = 'update',data ={'tagid':tagid,'tagname':tagname})
            else:
                print('tagid not found')
                return
        else:
            print('tagname not found')
            return

    
    def delete(self,tagid):
        # param tagid:标签ID
        tagidlist = [i['tagid'] for i in self.taglist()['taglist']]
        if tagid in tagidlist:
            return self.get_api(api = 'delete',query_params={'tagid':tagid})
        else:
            print('tag not found')
            return
    
    def get(self,tagid):
        # param tagid:标签ID
        tagidlist = [i['tagid'] for i in self.taglist()['taglist']]
        if tagid in tagidlist:
            return self.get_api(api = 'get',query_params={'tagid':tagid})
        else:
            return {'error':'Tag not found'}

    def addtagusers(self,tagid,userlist=None,partylist=None):
        """
        :param tagid: 标题id
        :param userlist:企业成员id列表，userlist,partylist不能同时为空
        :param partylist:企业部门id列表
        """
        # 读取config中的成员列表数据
        # 验证是否存在
        useridlist = _config.useridlist
        tagidlist = [i['tagid'] for i in self.taglist()['taglist']]
        userlist = [userlist]
        partyidlist = _config.partyidlist
        for i in userlist:
            if i in useridlist:
                if tagid in tagidlist:
                    WeChatWorkError.overlength(userlist,1000)
                    WeChatWorkError.overlength(partylist,100)
                    return self.post_api(api = 'addtagusers',data={'tagid':tagid,'userlist':userlist,'partylist':partylist})
                    # 逐层排查，返回空
                else:
                    return
            else:
                return

    def deltagusers(self,tagid,userlist=None,partylist=None):
        """
        :param tagid: 标题id
        :param userlist:企业成员id列表，userlist,partylist不能同时为空
        :param partylist:企业部门id列表 TODO:不能同时存在
        """
        # 读取config中的成员列表数据
        # 验证是否存在
        useridlist = _config.useridlist
        tagidlist = [i['tagid'] for i in self.taglist()['taglist']]
        userlist = [userlist]
        partyidlist = _config.partyidlist

        for i in userlist:
            if i in useridlist:
                if tagid in tagidlist:
                    WeChatWorkError.overlength(userlist,1000)
                    WeChatWorkError.overlength(partylist,100)
                    return self.post_api(api = 'deltagusers',data={'tagid':tagid,'userlist':userlist,'partylist':partylist})
                    # 逐层排查，返回空
                else:
                    return
            else:
                return


