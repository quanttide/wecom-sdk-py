# -*- coding: utf-8 -*-


from wecom_sdk.base.client import WeComBaseAPIClient
from .user import UserAPIMixin
from .department import DepartmentAPIMixin
from .tag import TagAPIMixin


class WecomContactAPIClient(WeComBaseAPIClient,
                            UserAPIMixin,
                            DepartmentAPIMixin,
                            TagAPIMixin
                            ):
    pass
