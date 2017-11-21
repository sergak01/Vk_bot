# -*- coding: utf-8 -*-
import settings
import random
import vk_api
from BotException import BotException

class Interface:
    vk = None
    vk_service = None
    dynamic_settings = dict()

    def __init__(self, vk, vk_service, dynamic_settings):
        self.vk = vk
        self.dynamic_settings = dynamic_settings
        self.vk_service = vk_service

    def get_keys(self):
        keys = [u'найди', u'поиск', u'найти', u'кино', u'фильм']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def get_rexp(self):
        r_keys = [["seach_hesh", r"(#[^,\n]*)"]]
        ret = {}
        for key in r_keys:
            ret[key[0]] = [self, key[1]]
        return ret

    def call(self, event):
        query = ""
        words = str(event.text).split()
        for word in words:
            if word.lower() not in self.get_keys():
                query += word + " "
        if query != "":
            self.vk.method('messages.send', {
                'user_id':int(event.user_id),
                'message':"Поисковый запрос: " + str(query)})
            #print(self.vk.method("groups.getById", {'v': "5.65"})[0].get("id"))
            random.seed()
            answer_count = self.vk_service.method(
                'wall.search',
                {
                'owner_id':"-" + str(self.vk.method(
                    "groups.getById",
                    {'v': "5.65"})[0].get("id")
                ),
                'query':str(query),
                'owners_only':1,
                'count':0,
                'offset':0
                }
                ).get("count")
            if answer_count > 0:
                answer = self.vk_service.method(
                    'wall.search',
                    {
                    'owner_id':"-" + str(self.vk.method(
                        "groups.getById",
                        {'v': "5.65"})[0].get("id")
                    ),
                    'query':str(query),
                    'owners_only':1,
                    'count':1,
                    'offset':random.randint(1, answer_count)
                    }
                    )
            else:
                answer = self.vk_service.method(
                    'wall.search',
                    {
                    'owner_id':"-" + str(self.vk.method(
                        "groups.getById",
                        {'v': "5.65"})[0].get("id")
                    ),
                    'query':str(query),
                    'owners_only':1,
                    'count':1,
                    'offset':0
                    }
                    )
            query = ""
            #print(answer)
            msg_search = ""
            if answer.get("items") != [] and answer.get("count") > 0:
                msg_search = "Ссылка на пост: https://vk.com/wall" + \
                    str(answer.get("items")[0].get("owner_id")) + "_" + \
                    str(answer.get("items")[0].get("id"))
                msg_search = msg_search + "\n\n" + \
                    answer.get("items")[0].get("text")[0:1000] + "..."
                attach_array = ""
                for attach in answer.get("items")[0].get("attachments"):
                    type_attach = attach.get("type")
                    attach_array += attach.get("type")
                    attach_array += str(
                        attach.get(type_attach).get("owner_id")
                        ) + "_"
                    attach_array += str(
                        attach.get(type_attach).get("id")
                        ) + "_"
                    attach_array += str(
                        attach.get(type_attach).get("access_key")
                        ) + ","
                #self.vk.method('messages.send', {'user_id':int(event.user_id),'message':str(attach_array)})
                self.vk.method('messages.send', {
                    'user_id':int(event.user_id),
                    'message':msg_search,
                    'attachment':attach_array
                    })
                self.vk.method('messages.send', {
                    'user_id':int(event.user_id),
                    'message':"Хочешь другой? Отправь запрос еще раз!"
                    })
            else:
                self.vk.method('messages.send', {
                    'user_id':int(event.user_id),
                    'message':"По вашему запросу ничего не найдено!" + \
                        " Попробуйте еще раз ;-)"
                    })
        else:
            self.vk.method('messages.send', {
                'user_id':int(event.user_id),
                'message':"Упс!😲 Вы забыли добавить название фильма!"
                })