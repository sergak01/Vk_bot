# -*- coding: utf-8 -*-

class Interface:
	vk = None
	dinamic_settings = dict()

	def __init__(self, vk, dinamic_settings):
		self.vk = vk
		self.dinamic_settings = dinamic_settings

	def get_keys(self):
		keys = [u'help', u'/help', u'помоги', u'помощь', u'допоможи', u'допомога', u'хелп', u'спасите', u'/помоги', u'/помощь', u'/допоможи', u'/допомога', u'/хелп', u'/спасите']
		ret = {}
		for key in keys:
			ret[key] = self
		return ret

	def get_rexp(self):
		return {}

	def call(self, msg):
		pass