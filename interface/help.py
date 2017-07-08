# -*- coding: utf-8 -*-

class Interface:
    vk = None
    dynamic_settings = dict()

    def __init__(self, vk, dynamic_settings):
        self.vk = vk
        self.dynamic_settings = dynamic_settings

    def get_keys(self):
        keys = [u'help', u'/help', u'помоги', u'помощь', u'допоможи', u'допомога', u'хелп', u'спасите', u'/помоги', u'/помощь', u'/допоможи', u'/допомога', u'/хелп', u'/спасите']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def get_rexp(self):
        return {}

    def call(self, msg):
        pass