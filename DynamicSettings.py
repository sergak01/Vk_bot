# -*- coding: utf-8 -*-
import re
import os

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
        raise NameError("Filename must be not empty!")

    def file_created(self):
            try:
                if os.stat(self.dynamic_settings_filename).st_size != 0:
                    return True
                else:
                    return False
            except FileNotFoundError:
                return False

    def get(self):
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
                return parameters_dict_temp
            else:
                return self.parameters_dict
        except FileNotFoundError:
            print("File not found!")
            return

    def set(self, settings={}):
        if isinstance(settings, dict):
            if settings == {}:
                settings = self.get()
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
                if self.get() == settings:
                    return
                else:
                    self.get()
                    for name, value in settings.items():
                        self.parameters_dict.update({name: value})
                    self.file = open(self.dynamic_settings_filename, "w")
                    parameters_dict_temp = self.parameters_dict.copy()
                    for item in self.file_data_list:
                        rexp_comment = r'^[#\s][^\n]+\n'
                        parser_c = re.compile(rexp_comment)
                        if parser_c.sub("", str(item))=="" or str(item)=="\n":
                            self.file.write(item)
                        else:
                            rexp = r'([^\s]+)[^\S]*=[^\S]*([^\n]+)\n?'
                            parser = re.compile(rexp)
                            for name, value in self.parameters_dict.items():
                                if (name == parser.sub(r'\1', str(item))) and \
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
            raise NameError("Settings not dict!")
        