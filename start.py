# -*- coding: utf-8 -*-
import time
from dynamic_settings import DynamicSettings
import ast

import settings

def main():
	'''Этот файл планируеться как основной стартовый модуль бота, который будет манипулировать файлом динамических настроек бота.
	На этой стадии файл динамических настроек включает такие переменные:
	users_token: тип данных dict - используеться для хранения временных токенов пользователей (планируеться использовать токены с временем
	жизни в 1 час), которые, в свою очередь, подтверждрают наличие у пользователя прав администратора.'''
	dyn_sett_dict = {}
	dyn_sett_file = DynamicSettings(dynamic_settings_filename = settings.dynamic_settings_file)
	if(dyn_sett_file.file_created()):
		dyn_sett_dict = dyn_sett_file.get_dynamic_settings()
	else:
		dyn_sett_dict = generate_standart_dynamic_setting()
		dyn_sett_file.set_dynamic_settings(dyn_sett_dict)
	temp_token_list = ast.literal_eval(dyn_sett_dict.get("users_token"))
	temp_token_list.update({50583928: "{user_token: token, time_out: 10}"})
	dyn_sett_dict.update({"users_token" : temp_token_list})
	dyn_sett_file.set_dynamic_settings(dyn_sett_dict)
	# while True:
	# 	setting = settings()
	# 	print_settings(setting)
	# 	time.sleep(10)
	# 	setattr(setting, "public_token", "token1")
	# d_sttings = dynamic_settings()
	print(str(dyn_sett_dict))

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