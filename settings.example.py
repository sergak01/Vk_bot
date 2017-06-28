# -*- coding: utf-8 -*-
#Бот предназначен только для сообществ с включенными сообщениями!
#Токен сообщества (обязательный параметр).
public_token = 'public/club token'
#ID вашего приложения ВК. -1 для использования стандартного app_id из vk_api (2895443)
#Оставьте -1, если не знаете что это.
#Приложение нужно для проверки на наличие у пользователя прав администратора сообщества
#и включения оповещений о сообщения в сообществе, а также возможности отправки сообщений
#пользователям через чат. Если равно -1, возможность взаимодействия через чат отключена.
vk_app_id = -1
#Переменная secret_key - тип str. Последовательность символов для начальной идентификации администратора. Передайте эту последовательность
#вашим администраторам, что-бы они смогли стать админами для бота.
secret_key = "1234567890"
#Пересылать сообщения только админам в онлайне. Если онлайн никого не будет, сообщения будут оправлены всем. False - пересылать всем подписаным
mail_admin_online = True
#Имя файла для хранения динамических настроек приложения. Данные в файл будут генерироваться автоматически.
dynamic_settings_file = 'dynamic_settings.ini'
#Папка интерфейсов
path = 'interface/'
#Префиксы сообщений, на которые бот будет реагировать.
#prefixes = ['lolbot', u'лолбот', u'лб', 'lb', u'фб', u'файнбот', 'fb', 'finebot', '!']
#Черный список пользователей (писать id аккаунта вк)
#blacklist = (0, 0)