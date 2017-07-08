# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import ast

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from DynamicSettings import DynamicSettings

import settings

def main():
    """Описание главного файла программы

    Этот файл планируеться как основной стартовый модуль бота, который
    будет манипулировать файлом динамических настроек бота. На этой
    стадии файл динамических настроек включает такие переменные: 
    users_token: тип данных dict - используеться для хранения
    временных токенов пользователей (планируеться использовать токены
    с временем жизни в 1 час), которые, в свою очередь, подтверждрают
    наличие у пользователя прав администратора.

    """
    dyn_sett_dict = {} #Словарь динамических настроек
    commands = {} #Словарь команд
    rexp_commands = {} #Словарь регулярных команд
    interfaces = {} #Словарь интерфейсов
    vk = vk_api.VkApi(token = settings.vk_token)
    settings.dyn_sett_file = DynamicSettings(dynamic_settings_filename = settings.dynamic_settings_file)
    dyn_sett_file = settings.dyn_sett_file
    if(dyn_sett_file.file_created()):
        dyn_sett_dict = dyn_sett_file.get()
    else:
        dyn_sett_dict = generate_standart_dynamic_setting()
        dyn_sett_file.set(dyn_sett_dict)

    try:
        vk.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    print('Подгружаем плагины...')

    print('---------------------------')

    # Подгружаем плагины
    sys.path.insert(0, settings.path)
    for f in os.listdir(settings.path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            interfaces[fname] = mod.Interface(vk, dyn_sett_dict)
    sys.path.pop(0)

    print('---------------------------')

    # Регистрируем ключевые слова интерфейсов
    for interface in interfaces.values():
        for key, value in interface.get_keys().items():
            commands[key] = value

    # Регистрируем регулярные слова интерфейсов
    for interface in interfaces.values():
        for key, value in interface.get_rexp().items():
            rexp_commands[key] = value

    #print(commands)
    #print(rexp_commands)

    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', end='')
            if event.from_user:
                print(event.user_id)
                command(event, commands, rexp_commands)

            try:
                print('Текст: ', event.text)
            except Exception as e:
                print(e)
                if e == KeyboardInterrupt:
                    return
            print()
        else:
            print(event.type, event.raw[1:])
    # temp_token_list = ast.literal_eval(dyn_sett_dict.get("users_token"))
    # temp_token_list.update({50583928: "{user_token: token, time_out: 10}"})
    # dyn_sett_dict.update({"users_token" : temp_token_list})
    # dyn_sett_file.set_dynamic_settings(dyn_sett_dict)
    # while True:
    #     setting = settings()
    #     print_settings(setting)
    #     time.sleep(10)
    #     setattr(setting, "public_token", "token1")
    # d_sttings = dynamic_settings()
    print(str(dyn_sett_dict))

def command(event, commands, rexp_commands):
    if event.text == u'':
        return
    words = event.text.split()
    if words[0].lower() in commands:
        commands[words[0].lower()].call(event)
    else:
        for key, value in rexp_commands.items():
            parser = re.compile(value[1])
            if parser.sub("", event.text) == "":
                rexp_commands[key][0].call(event)

def print_settings(obj_settings):
    print(str(getattr(obj_settings, "users_token")))
    print(str(getattr(obj_settings, "answer_admins")))
    print(str(getattr(obj_settings, "mail_subscription_admins")))

def generate_standart_dynamic_setting():
    temp_dict = dict()
    temp_dict.update({"users_token": str(dict())})
    temp_dict.update({"answer_admins": str(list())})
    temp_dict.update({"mail_subscription_admins": str(list())})
    return temp_dict


if __name__ == '__main__':
    main()