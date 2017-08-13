# -*- coding: utf-8 -*-
from BotException import BotException

class Interface:
    vk = None
    dynamic_settings = dict()

    def __init__(self, vk, vk_service, dynamic_settings):
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

    def call(self, event):
        self.vk.method('messages.send', {'user_id':int(event.user_id),'message':"Если вы хотите найти фильм и отправляете просто его название, ничего не выйдет. Нужно до названия фильма добавлять слово \"Найди\" или символ \"#\" перед первым словом."})