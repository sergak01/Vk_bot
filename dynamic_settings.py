# -*- coding: utf-8 -*-
import re
import os

class DynamicSettings:
	dynamic_settings_filename = ""
	file = ""
	file_opened = False
	file_data_list = []
	parameters_dict = {}

	def __init__(self, dynamic_settings_filename = "dynamic_settings.ini"):
		self.dynamic_settings_filename = dynamic_settings_filename

	def get_dict(self):
		return self.parameters_dict

	def file_created(self):
		try:
			if os.stat(self.dynamic_settings_filename).st_size != 0:
				return True
			else:
				return False
		except FileNotFoundError:
			return False

	def set_filename(self, filename):
		if filename == "":
			raise NameError("Filename must be not empty!")
		self.dynamic_settings_filename = filename

	def open_file(self, parametr = "r"):
		'''Немного модифицированная стандартная функция открытия файла. Дает классу знание об открытости файла для записи.
		Возвращает ссылку на файл, если с ним нужны манипуляции вне класса. Внутри класса файл будет открыт до вызова команды
		close_file() из экземпляра класса.
		Warning: Не закрывайте файл стандартной функцией close() через его идентификатор! Это, скорее всего, приведет к парочке исключений!'''
		if parametr == "":
			raise NameError("Parametr must be not empty!")
		self.file = open(self.dynamic_settings_filename, parametr)
		self.file_opened = True
		return self.file

	def close_file(self):
		'''Функция закрытия файла динамических настроек.'''
		self.file.close()
		self.file_opened = False

	def get_dynamic_settings(self):
		'''Функция для получения динамических настроек с файла. Возвращает словарь, который содержит все переменные, что находяться в файле.
		Этот словарь будет актуальным тольки при запуске программы или инициализации класса. Перед вызовом стоит убедиться что файл существует
		и он не пустой. Для этого вызываем функцию file_created() из экземпляра класса. Если она возвращает False, генерируем не пустой dict()
		и передаем его экземпляру класса через функцию set_dynamic_settings().
		Во время работы программы, если мы точно знаем что файл не исчез, функция используеться для обновления массива строк с файла. 
		Каждый запуск обновляет переменную file_data_list, экземпляра класса.'''
		if os.stat(self.dynamic_settings_filename).st_size != 0:
			self.open_file("r")
			if self.file_opened == False:
				self.close_file()
				raise NameError('File must be opened!')
			else:
				self.file_data_list = self.file.readlines()
				parameters_dict_temp = self.parameters_dict.copy()
				for item in self.file_data_list:
					if item[0] != '#' and item[0] != '\n' and item[0] != ' ':
						rexp = r'([^ \n\t]+)[^=]*=[^\S]*([^\n]+)\n*'
						parser = re.compile(rexp)
						parameters_dict_temp.update({parser.sub(r'\1', str(item)): parser.sub(r'\2', str(item))})
				self.close_file()
				return parameters_dict_temp
		else:
			raise NameError("File is empty!")

	def set_dynamic_settings(self, this_dict = {}):
		if this_dict == {}:
			this_dict = self.get_dict()
		try:
			os.stat(self.dynamic_settings_filename).st_size
		except FileNotFoundError:
			self.open_file("w")
			self.close_file()
		if os.stat(self.dynamic_settings_filename).st_size == 0:
			self.open_file("w")
			if self.file_opened == False:
				self.close_file()
				raise NameError("File not opened for writing!")
			else:
				for name, value in this_dict.items():
					self.file.write(str(name) + " = " + str(value))
					self.file.write('\n')
				self.close_file()
		else:
			if self.get_dynamic_settings() == this_dict:
				return True
			else:
				self.get_dynamic_settings()
				for name, value in this_dict.items():
					self.parameters_dict.update({name: value})
				self.open_file("w")
				if self.file_opened == False:
					self.close_file()
					raise NameError("File not opened for writing!")
				else:
					parameters_dict_temp = self.parameters_dict.copy()
					for item in self.file_data_list:
						rexp_comment = r'^[#\s][^\n]+\n'
						parser_c = re.compile(rexp_comment)
						# print(str(item))
						if parser_c.sub("", str(item)) == "" or str(item) == "\n":
							self.file.write(item)
						else:
							rexp = r'([^\s]+)[^\S]*=[^\S]*([^\n]+)\n?'
							parser = re.compile(rexp)
							for name, value in self.parameters_dict.items():
								if name == parser.sub(r'\1', str(item)) and name != '':
									# print(value)
									self.file.write(str(name) + " = " + str(value))
									self.file.write('\n')
									parameters_dict_temp.pop(name, str(""))
									break;
					for name, value in parameters_dict_temp.items():
						if name != "":
							self.file.write(str(name) + " = " + str(value))
							self.file.write('\n')
					self.close_file()


	def get_file(self):
		if self.file_opened == True:
			return self.file
		else:
			raise NameError('File not opened!')