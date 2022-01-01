# -*- coding: utf-8 -*-


class ServiceAPIMixin(object):
    def request_service_api(self, method, api, query_params=None, data=None):
        api = 'service' + api
        return self.request_api(method, api, query_params, data)
