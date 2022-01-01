# -*- coding: utf-8 -*-


class TagAPIMixin(object):
    """
    标签管理API
    """
    # --- 通用API ---
    def request_tag_api(self, method, api, query_params=None, data=None):
        api = 'tag/' + api
        return self.request_api(method, api, query_params, data)

    def get_tag_api(self, api, query_params=None, data=None):
        return self.request_tag_api('GET', api, query_params, data)

    def post_tag_api(self, api, query_params=None, data=None):
        return self.request_tag_api('POST', api, query_params, data)

    # --- API ---
    def get_members_by_tag_id(self, tag_id):
        """
        获取标签成员
        """
        return self.get_tag_api(api='get', query_params={'tagid': tag_id})

    def get_tag_list(self):
        """
        获取标签列表
        """
        return self.get_tag_api(api='list')['taglist']

    # --- high-level API ---
    def find_tag_id_by_name(self, tag_name, tag_list=None):
        """

        """
        if tag_list is None:
            tag_list = self.get_tag_list()
        for item in tag_list:
            if item['tagname'] == tag_name:
                return item['tagid']
        # TODO: 更换准确的Exception类。
        raise Exception(f'Cannot find `tag_id` with `tag_name`={tag_name}')

    def get_members_by_tag_name(self, tag_name):
        """
        通过标签名获取标签成员
        """
        tag_id = self.find_tag_id_by_name(tag_name)
        return self.get_members_by_tag_id(tag_id)
