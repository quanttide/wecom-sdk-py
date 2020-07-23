# -*- coding: utf-8 -*-


class ValidationMixin(object):
    def validate_userid(self):
        pass

    def validate(self, **kwargs):
        for key, value in kwargs.items():
            validate_attr = 'validate_' + key
            if hasattr(self, validate_attr):
                self.__getattribute__(validate_attr)(value)

