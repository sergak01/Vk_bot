# -*- coding: utf-8 -*-
from BotException import BotException

class Interface:
    vk = None
    dynamic_settings = dict()

    def __init__(self, vk, vk_service, dynamic_settings):
        self.vk = vk
        self.dynamic_settings = dynamic_settings

    def get_keys(self):
        keys = [u'привет', u'здраствуйте', u'hello', u'hi']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def get_rexp(self):
        return {}

    def call(self, event):
        msg = "Привет! \nЯ бот сообщества Кино Империя!\nМой функционал сейчас в разработке и я могу немного." + \
        "\nЕсли хочешь что-бы я нашел для тебя фильм, напиши мне такое сообщение:\nНайди (название фильма)\n" + \
        "Писать нужно без скобок.\nТакже я могу найти фильм по хештегу жанра. Например: #боевик\n" + \
        "Если что-то не будет получаться - напишите мне: помоги или help"
        self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})