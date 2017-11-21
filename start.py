# -*- coding: utf-8 -*-
import os
import sys
import re
import time
import ast

from difflib import SequenceMatcher
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from DynamicSettings import DynamicSettings
from BotException import BotException

import settings

db_driver = settings.db_driver

print("Импортируем драйвер базы данных.")
if db_driver == "sqlite3":
    #if SQLite
    import sqlite3
    print("Импортирован драйвер SQLite")
elif db_driver == "psycopg2":
    #if PostgreSQL
    import psycopg2
    print("Импортирован драйвер PostgreSQL")
elif db_driver == "mysql.connector":
    #if MySQL
    import mysql.connector
    print("Импортирован драйвер MySQL")
elif db_driver == "pyodbc":
    #if ODBC
    import pyodbc
    print("Импортирован драйвер ODBC")
else:
    print("Драйвер базы данных не поддерживаеться!")
    quit()

def main(developing=False, longpoll=None):
    """Описание главного файла программы

    Этот файл планируеться как основной стартовый модуль бота, который
    будет манипулировать файлом динамических настроек бота. На этой
    стадии файл динамических настроек включает такие переменные: 
    users_token: тип данных dict - используеться для хранения
    временных токенов пользователей (планируеться использовать токены
    с временем жизни в 1 час), которые, в свою очередь, подтверждрают
    наличие у пользователя прав администратора.

    """
    if developing:
        print("Я запущен в режиме разработчика. Делай со мной все что хочешь :-)")
        print("Подключаем базу данных")
        db_connector = sqlite3.connect(settings.db_name)
        print("База данных успешно подключена")
        print("Инициализируем курсор")
        db_cursor = db_connector.cursor()
        print("Курсор готов")
        # Работа с базой данных
        user_command = 'найдите'
        db_cursor.execute(
            "SELECT * FROM command WHERE new_command='" + \
                user_command + "';"
        )
        # print(db_cursor.fetchall())
        db_result = db_cursor.fetchall()
        if db_result:
            print(db_result[0][0])
        else:
            db_cursor.execute("SELECT * FROM command")
            db_result = db_cursor.fetchall()
            max_ratio = ["item", "user_command", 0]
            for item in db_result:
                s = SequenceMatcher(lambda x: x==" ", item[1], user_command)
                if max_ratio[2] < s.ratio():
                    max_ratio[0] = (item[0], item[1])
                    max_ratio[1] = user_command
                    max_ratio[2] = s.ratio()
                print("Ratio: " + item[1] + " and " + user_command + \
                    ": " + str(s.ratio()))
            print("Max ratio: " + str(max_ratio[0]) + " and " + max_ratio[1] + \
                ": " + str(max_ratio[2]))
            if max_ratio[2] >= 0.7 and len(max_ratio[1]) > 3:
                db_cursor.execute("INSERT INTO command (standart_command," + \
                    " new_command) VALUES ('" + max_ratio[0][0] + "', '" + \
                    max_ratio[1] + "');"
                )
                db_connector.commit()
                print("Спасибо, я выучил кое-что новое ;-)")
        # print(db_cursor.fetchall()[0][0])
        #----------------------
        print("Отключаем базу данных")
        db_connector.close()
    try:
        dyn_sett_dict = {} #Словарь динамических настроек
        commands = {} #Словарь команд
        rexp_commands = {} #Словарь регулярных команд
        interfaces = {} #Словарь интерфейсов
        vk = vk_api.VkApi(token = settings.vk_token)
        dynamic_settings = DynamicSettings(
            dynamic_settings_filename = settings.dynamic_settings_file
            )
        if(dynamic_settings.file_created()):
            dyn_sett_dict = dynamic_settings.get()
        else:
            dyn_sett_dict = generate_standart_dynamic_setting()
            dynamic_settings.set(dyn_sett_dict)

        try:
            vk.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        vk_service = vk_api.VkApi(token = settings.service_key)
        try:
            vk_service.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        print('Подгружаем интерфейсы...')

        print('---------------------------')

        # Подгружаем плагины
        sys.path.insert(0, settings.path)
        for f in os.listdir(settings.path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(fname)
                interfaces[fname] = mod.Interface(
                    vk, vk_service,
                    dynamic_settings
                )
        sys.path.pop(0)

        # Регистрируем ключевые слова интерфейсов
        for interface in interfaces.values():
            for key, value in interface.get_keys().items():
                commands[key] = value

        #print(commands)

        # Регистрируем регулярные слова интерфейсов
        for interface in interfaces.values():
            for key, value in interface.get_rexp().items():
                rexp_commands[key] = value

        #print(rexp_commands)

        print('---------------------------')
        print('Интерфейсы загружены')

        #print(commands)
        #print(rexp_commands)
        print('Запускаем постоянное считывание ленты сообщений...')
        if longpoll == None:
            longpoll = VkLongPoll(vk)
        else:
            longpoll.update_longpoll_server()
        print('Считывание ленты запущено.')
        for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    print('Новое сообщение:')
                    if event.to_me:
                        print('Для меня от: ', end='')
                        print(str(event.user_id))
                        if not_sticker(vk, event):
                            command(event, commands, rexp_commands, vk)
                    elif event.from_me:
                        print('От меня для: ', end='')
                        print(str(event.user_id))
                        
                    try:
                        print('Текст: ', event.text)
                    except UnicodeEncodeError as e:
                        print(e)
                    except KeyboardInterrupt:
                        print("Процесс бота завершен пользователем!")
                        raise
                    except Exception as e:
                        print(e)
                        raise
                    print()
                else:
                    print(event.type, event.raw[1:])
    except Exception as e:
        print(e)
        time.sleep(10)
        main(developing=developing, longpoll=longpoll)

def not_sticker(vk, event):
    rep_rexp_type = r'attach(\d)_type'
    pars = re.compile(rep_rexp_type)
    for key, value in event.attachments.items():
        if pars.sub("", key) == "" and value == "sticker":
            print(vk.method('messages.send', {
                'user_id':event.user_id,
                'message':'Извините, бот не поддерживает стикеры.',
                'forward_messages':event.raw[1]
            }))
            return False
    return True

def command(event, commands, rexp_commands, vk):
    if event.text == u'':
        return
    words = event.text.split()
    for word in words:
        if word.lower() in commands:
            print("Найдена команда: " + str(word.lower()))
            commands[word.lower()].call(event)
            print("Команда сработала")
            return
        else:
            for key, value in rexp_commands.items():
                parser = re.compile(value[1])
                if parser.sub("", word) == "":
                    print("Найдена команда: " + str(rexp_commands[key][1]))
                    rexp_commands[key][0].call(event)
                    print("Команда сработала")
                    return
    vk.method('messages.send', {
        'user_id':int(event.user_id),
        'message':"Я не знаю такой команды! Напиши привет, что-бы узнать" + \
            " что я умею :-)"
        })


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
    if len (sys.argv) > 1:
        for param in sys.argv:
            if param == "-dev" or param == "-developing":
                main(developing=True)
    else:
        main()