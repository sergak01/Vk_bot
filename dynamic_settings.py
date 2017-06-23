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
		if os.stat(self.dynamic_settings_filename).st_size != 0:
			return True
		else:
			return False

	def set_filename(self, filename):
		if filename == "":
			raise NameError("Filename must be not empty!")
		self.dynamic_settings_filename = filename

	def open_file(self, parametr = "r"):
		if parametr == "":
			raise NameError("Parametr must be not empty!")
		self.file = open(self.dynamic_settings_filename, parametr)
		self.file_opened = True
		return self.file

	def close_file(self):
		self.file.close()
		self.file_opened = False

	def get_dynamic_settings(self):
		if os.stat(self.dynamic_settings_filename).st_size != 0:
			self.open_file("r")
			if self.file_opened == False:
				self.close_file()
				raise NameError('File must be opened!')
			else:
				self.file_data_list = self.file.readlines()
				for item in self.file_data_list:
					if item[0] != '#':
						rexp = r'([^ \n\t]+) = ([^\n]+)'
						parser = re.compile(rexp)
						self.parameters_dict.update({parser.sub(r'\1', str(item)): parser.sub(r'\2', str(item))})
						return self.parameters_dict
				self.close_file()
		else:
			raise NameError("File is empty!")

	def set_dynamic_settings(self, this_dict = {}):
		if this_dict == {}:
			this_dict = self.get_dict()
		if os.stat(self.dynamic_settings_filename).st_size == 0:
			self.open_file("w")
			if self.file_opened == False:
				self.close_file()
				raise NameError("File not opened for writing!")
			else:
				for name, value in this_dict.items():
					self.file.write(str(name) + " = " + str(value) + "\n")
				self.close_file()
		else:
			if self.get_dynamic_settings() == this_dict:
				return True
			else:
				self.get_dynamic_settings()
				for name, value in this_dict.items():
					self.parameters_dict.update(name, value)
				self.open_file("w")
				if self.file_opened == False:
					self.close_file()
					raise NameError("File not opened for writing!")
				else:
					for name, value in self.parameters_dict.items():
						self.file.write(str(name) + " = " + str(value) + "\n")
					self.close_file()


	def get_file(self):
		if self.file_opened == True:
			return self.file
		else:
			raise NameError('File not opened!')