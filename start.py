# -*- coding: utf-8 -*-
import time
from dynamic_settings import DynamicSettings

import settings

def main():
	dyn_sett_dict = {}
	dyn_sett_file = DynamicSettings(dynamic_settings_filename = settings.dynamic_settings_file)
	if(dyn_sett_file.file_created()):
		dyn_sett_dict = dyn_sett_file.get_dynamic_settings()
	else:
		dyn_sett_dict = generate_standart_dynamic_setting()
		dyn_sett_file.set_dynamic_settings(dyn_sett_dict)
	# while True:
	# 	setting = settings()
	# 	print_settings(setting)
	# 	time.sleep(10)
	# 	setattr(setting, "public_token", "token1")
	# d_sttings = dynamic_settings()

def print_settings(obj_settings):
	print(str(getattr(obj_settings, "answer_admins")))
	print(str(getattr(obj_settings, "mail_subscription_admins")))
	print(str(getattr(obj_settings, "mail_admin_online")))

def generate_standart_dynamic_setting():
	temp_dict = dict()
	temp_dict.update({"users_token": str(dict())})
	temp_dict.update({"answer_admins": str(list())})
	temp_dict.update({"mail_subscription_admins": str(list())})
	return temp_dict


if __name__ == '__main__':
	main()