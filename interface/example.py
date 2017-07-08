# -*- coding: utf-8 -*-

class Interface:
    vk = None
    dynamic_settings = dict()

    def __init__(self, vk, dynamic_settings):
        self.vk = vk
        self.dynamic_settings = dynamic_settings

    def get_keys(self):
        keys = [u'example_interface', u'пример_интерфейса']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def get_rexp(self):
        return {}

    def call(self, msg):
        pass