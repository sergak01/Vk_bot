# -*- coding: utf-8 -*-
import re
import os
import time
import ast

from BotException import BotException

class DynamicSettings:
    """Класс для управления динамическими настройками бота.

    Позволяет сохранять, редактировать, считывать и работать с
    динамическими настройками бота.

    Инициация класса без параметров присваевает переменной
    dynamic_settings_filename стандартное значение имени файла для
    сохранения динамических настроек, а именно: dynamic_settings.ini
    
    """
    dynamic_settings_filename = ""
    file = ""
    file_data_list = list()
    parameters_dict = dict()

    def __init__(self, dynamic_settings_filename="dynamic_settings.ini"):
        self.dynamic_settings_filename = dynamic_settings_filename
        self.parameters_dict = self.get().copy()
        if self.parameters_dict != self.get(original = True):
            self.set(self.parameters_dict)

    def set_filename(self, filename="dynamic_settings.ini"):
        """Изменение стандартного имени файла динамических настроек

        Если вызвать функцию без параметров - сбрасывает имя на
        стандартное.

        При вызове функции с пустым именем файла - бросает исключение:
        'Filename must be not empty!'

        """
        if filename != "":
            self.dynamic_settings_filename = filename
            return
        raise BotException("Filename must be not empty!")

    def file_created(self):
        """Функция проферки существования файла динамических настроек.

        Возвращает True если файл существуеи и он не пустой.
        Иначе - возвращает False

        """
        try:
            if os.stat(self.dynamic_settings_filename).st_size != 0:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def get(self, original=False):
        """Возвращает словарь с настройками

        Параметр original принимает значение True или False.

        Когда равно True - возвращает оригинальные настройки, иначе
        проверяет валидность токенов по времени жизни. Если время
        жизни менше в unixtime чем сейчас - удаляет токен.

        """
        try:
            if os.stat(self.dynamic_settings_filename).st_size != 0:
                self.file = open(self.dynamic_settings_filename, "r")
                self.file_data_list = self.file.readlines()
                parameters_dict_temp = self.parameters_dict.copy()
                for item in self.file_data_list:
                    if item[0]!='#' and item[0]!='\n' and item[0]!=' ':
                        rexp = r'([^ \n\t]+)[^=]*=[^\S]*([^\n]+)\n*'
                        parser = re.compile(rexp)
                        parameters_dict_temp.update({
                            parser.sub(r'\1', str(item)):
                            parser.sub(r'\2', str(item))}
                            )
                self.file.close()
                if not original:
                    self.autoremove(parameters_dict = parameters_dict_temp)
                return parameters_dict_temp
            else:
                if not original:
                    self.autoremove()
                return self.parameters_dict
        except FileNotFoundError:
            print("File not found!")
            if not original:
                self.autoremove()
            return self.parameters_dict

    def set(self, settings={}):
        """Сохраняет настройки в переменную и записывает в файл

        Если функция выполнена без параметров или передан пустой
        словарь - получает настройки выполнением функции get() без
        параметров.

        Также, если файл динамических настроек не существует - создает
        его.

        Когда файл существует и он пустой - пишет в файл содержимое
        параметра settings без каких либо изменений.

        Если файл не пустой - проверяет настройки на обработку
        функцией autoremove() сравнением словарей settings и
        возвращаемым значением функции get(original = True). Если они
        будут равны - ничего не делает, так-как настройки одинаковые.
        Если настройки отличаються - выполняет обновление переменной и
        файла, не затронув комментарии.

        Поддерживаються только однострочные комментарии, где началом
        строки (обязательно первым символом) должен идти знак решетки
        '#'. Если будут отличия - возможны баги и удаление этих строк.

        """
        if isinstance(settings, dict):
            # self.autoremove(parameters_dict = settings)
            if settings == {}:
                settings = self.get()
                # self.autoremove(parameters_dict = settings)
            try:
                os.stat(self.dynamic_settings_filename).st_size
            except FileNotFoundError:
                self.file = open(self.dynamic_settings_filename, "w")
                self.file.close()
            if os.stat(self.dynamic_settings_filename).st_size == 0:
                self.file = open(self.dynamic_settings_filename, "w")
                for name, value in settings.items():
                    self.file.write(str(name) + " = " + str(value))
                    self.file.write('\n')
                self.file.close()
            else:
                if self.get(original = True) == settings:
                    return
                else:
                    self.get(original = True)
                    for name, value in settings.items():
                        self.parameters_dict.update({name: value})
                    self.file = open(
                        self.dynamic_settings_filename, 
                        "w"
                        )
                    parameters_dict_temp = self.parameters_dict.copy()
                    for item in self.file_data_list:
                        rexp_comment = r'^[#\s][^\n]+\n'
                        parser_c = re.compile(rexp_comment)
                        if parser_c.sub("", str(item))=="" or \
                            str(item)=="\n":
                            self.file.write(item)
                        else:
                            rexp = r'([^\s]+)[^\S]*=[^\S]*([^\n]+)\n?'
                            parser = re.compile(rexp)
                            for name, value in \
                                self.parameters_dict.items():
                                if (name==parser.sub(r'\1', str(item))) and \
                                    (name != ''):
                                    self.file.write(str(name) +
                                        " = " +
                                        str(value))
                                    self.file.write('\n')
                                    parameters_dict_temp.pop(name, str(""))
                                    break;
                    for name, value in parameters_dict_temp.items():
                        if name != "":
                            self.file.write(str(name) + " = " + str(value))
                            self.file.write('\n')
                    self.file.close()
        else:
            raise BotException("Settings not dict!")

    def autoremove(self, parameters_dict=parameters_dict):
        """Функция удаляет токены с вышедшим временем time_out

        Функцию возможно запускать без параматров, тогда она проверит
        'умершие' токены и удалит их в файле динамических настроек.

        Если передать в параметре parameters_dict словарь, функция
        его проверит на мертвые токены и обновит.

        """
        users_token = ast.literal_eval(
            parameters_dict.get("users_token")
            ).copy()
        users_token_temp = ast.literal_eval(
            parameters_dict.get("users_token")
            ).copy()
        for key, value in users_token_temp.items():
            if isinstance(
                ast.literal_eval(ast.literal_eval(value).get("time_out")),
                int
                ) and (ast.literal_eval(
                ast.literal_eval(value)["time_out"]) < \
                int(time.time())
                ):
                users_token.pop(key, False)
        parameters_dict.update({"users_token": str(users_token)})
        # print(parameters_dict)

    def update(self, item=dict):
        """Функция обновляет своварь настроек

        Для работы принимает словарь item и обновляет функцикй update()
        словарь настроек.

        Если item не будет типа dict, выкинет BotException с строкой
        'Item not dict!'

        """
        if isinstance(item, dict) and item!={}:
            self.parameters_dict.update(item)
            self.set(settings = self.parameters_dict)
            return
        raise BotException("Item not dict!")
        