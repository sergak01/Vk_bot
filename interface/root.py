# -*- coding: utf-8 -*-
import settings
import urllib.request, json
import re
import time
import ast
import vk_api

class Interface:
	vk = None
	dinamic_settings = dict()

	def __init__(self, vk, dinamic_settings):
		self.vk = vk
		self.dinamic_settings = dinamic_settings

	def get_keys(self):
		keys = [settings.secret_key]
		ret = {}
		for key in keys:
			ret[key] = self
		return ret

	def get_rexp(self):
		r_keys = [["code", r"https:\/\/oauth\.vk\.com\/blank\.html#code=([^$]+)"]]
		ret = {}
		for key in r_keys:
			ret[key[0]] = [self, key[1]]
		return ret

	def call(self, event):
		try:
			for key, value in ast.literal_eval(str(self.dinamic_settings['users_token'])).items():
				if event.user_id == ast.literal_eval(key):
					group_id = self.vk.method("groups.getById", {'v': "5.65"})
					# print(ast.literal_eval(value)['user_token'])
					vk_user = vk_api.VkApi(token = ast.literal_eval(value)['user_token']) #нужно организовать удаление токена
					try:
						vk_user.auth()
					except vk_api.AuthError as error_msg:
						msg = "Не могу авторизироваться по вашему токену. Пройдите авторизацию заново!\nОшибка: " + str(error_msg)
						self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})
						return
					is_admin = vk_user.method("groups.getById", {'group_id': group_id[0]['id'], 'fields': 'is_admin', 'v': "5.65"})[0]['is_admin']
					if is_admin == 1:
						temp_answer_admins = ast.literal_eval(str(self.dinamic_settings['answer_admins']))
						if not (str(event.user_id) in temp_answer_admins):
							temp_answer_admins.append(str(event.user_id))
						self.dinamic_settings.update({'answer_admins': temp_answer_admins})
						settings.dyn_sett_file.set_dynamic_settings(self.dinamic_settings)
						msg = "Права администратора успешно получены!"
						self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})
						return
			raise NameError("No token for this user!")
		except Exception as e:
			print(e)
			user_code = ""
			for key, value in self.get_rexp().items():
				parser = re.compile(value[1])
				if parser.sub("", event.text) == "" and key == "code":
					user_code = parser.sub(r'\1', event.text)
			if user_code == "":
				msg = "https://oauth.vk.com/authorize?client_id=" + str(settings.vk_app_id) + "&scope=groups&display=page&response_type=code&v=5.65\n" + \
				"Для получения прав админа в боте нужно скопировать ссылку, вставить ее в новой вкладке в поле ввода адреса и перейти по ссылке.\n" + \
				"Как только загрузка закончиться, нужно скопировать ссылку из адресной строки и передать ее боту через чат.\n" + \
				"Данные в ссылке будут рабочими только один час."
				self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})
			else:
				url = "https://oauth.vk.com/access_token?client_id=" + str(settings.vk_app_id) + \
				"&client_secret=" + str(settings.secret_app_key) + "&code=" + str(user_code)
				print(url)
				try:
					with urllib.request.urlopen(url) as url:
						data = json.loads(url.read().decode())
						temp_token_list = ast.literal_eval(str(self.dinamic_settings.get("users_token")))
						temp_token_list.update({"" + str(data['user_id']) + "": "{'user_token': '" + 
							data['access_token'] + "', 'time_out': '" + str(int(time.time()) + 
								int(data['expires_in'])) + "'}"})
						self.dinamic_settings.update({'users_token': temp_token_list})
						settings.dyn_sett_file.set_dynamic_settings(self.dinamic_settings)
						msg = "Ваш токен получен! Проверяем на наличие прав админа..."
						self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})
						vk_user = vk_api.VkApi(token = data['access_token'])
						try:
							vk_user.auth()
						except vk_api.AuthError as error_msg:
							msg = "Не могу авторизироваться по вашему токену. Пройдите авторизацию заново!\nОшибка: " + str(error_msg)
							self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})
							return
						is_admin = vk_user.method("groups.getById", {'group_id': group_id[0]['id'], 'fields': 'is_admin', 'v': "5.65"})[0]['is_admin']
						if is_admin == 1:
							temp_answer_admins = ast.literal_eval(self.dinamic_settings['answer_admins'])
							if not (str(event.user_id) in temp_answer_admins):
								temp_answer_admins.append(str(event.user_id))
							self.dinamic_settings.update({'answer_admins': temp_answer_admins})
							settings.dyn_sett_file.set_dynamic_settings(self.dinamic_settings)
							msg = "Права администратора успешно получены!"
							self.vk.method('messages.send', {'user_id':int(event.user_id),'message':msg})
							return
				except  Exception as e:
					self.vk.method('messages.send', {'user_id':int(event.user_id),'message':e})