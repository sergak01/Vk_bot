# -*- coding: utf-8 -*-

class Interface:
	vk = None
	dinamic_settings = dict()

	def __init__(self, vk, dinamic_settings):
		self.vk = vk
		self.dinamic_settings = dinamic_settings

	def get_keys(self):
		keys = [u'example_interface', u'пример_интерфейса']
		ret = {}
		for key in keys:
			ret[key] = self
		return ret

	def get_rexp(self):
		return {}

	def call(self, msg):
		pass