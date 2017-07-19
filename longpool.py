# -*- coding: utf-8 -*-
import vk_api
import re
import time
from vk_api.longpoll import VkLongPoll, VkEventType

import settings

def write_msg(user_id, s, vk_session, forward_messages=""):
    if forward_messages == "":
        vk_session.method('messages.send', {'user_id':user_id,'message':s})
    else:
        vk_session.method('messages.send', {'user_id':user_id,'message':s,'forward_messages':forward_messages})

def main(longpoll=None):
    try:
        """ Пример использования longpoll
            https://vk.com/dev/using_longpoll
            https://vk.com/dev/using_longpoll_2
        """

        #login, password = '', ''
        #vk_session = vk_api.VkApi(login, password)
        print("Запускаю новую сессию!")
        token = settings.vk_token
        vk_session = vk_api.VkApi(token = token)
        vk_user_session = vk_api.VkApi(token = settings.vk_user_token)
        vk_empty_session = vk_api.VkApi()

        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        if longpoll == None:
            longpoll = VkLongPoll(vk_session)
        else:
            longpoll.update_longpoll_server()

        for event in longpoll.listen():
            try:
                if event.type == VkEventType.MESSAGE_NEW:
                    print('Новое сообщение:')

                    if event.from_me:
                        print('От меня для: ', end='')
                    elif event.to_me:
                        print('Для меня от: ', end='')

                    if event.from_user:
                        print(event.user_id)
                        if int(event.user_id) == 57008075:
                            reg = r'(id)?(\d*)? ?([^$]+)'
                            parser=re.compile(reg)
                            answer = parser.sub(r'\2', str(event.text))
                            if answer != "":
                                answer = parser.sub(r'\2', str(event.text))
                                try:
                                    if parser.sub(r'\3', str(event.text)) != "":
                                        write_msg(int(answer), parser.sub(r'\3', str(event.text)), vk_session)
                                    else:
                                        write_msg(int(answer), u".", vk_session)
                                except Exception as e:
                                    print(e)
                                user_name = vk_empty_session.method('users.get', {'user_id':int(answer)})
                                write_msg(57008075, u'Сообщение отправлено пользователю [id' + str(answer) + u'|' + 
                                    str(user_name[0]["first_name"]) + " " + str(user_name[0]["last_name"]) + 
                                    ']', vk_session)
                                continue;
                    elif event.from_chat:
                        print(event.user_id, 'в беседе', event.chat_id)
                    elif event.from_group:
                        print('группы', event.group_id)
                    try:
                        print('Текст: ', event.text)
                    except Exception as e:
                        print(e)
                    print()
                    if not event.from_me:
                        user_name = vk_empty_session.method('users.get', {'user_id':int(event.user_id)})
                        write_msg(57008075, u'[id' + str(event.user_id) + u'|' + 
                            str(user_name[0]["first_name"]) + " " + 
                            str(user_name[0]["last_name"]) +'] написал: ' + 
                            str(event.text) + '\nОтветить: https://vk.com/gim90818758?sel=' + 
                            str(event.user_id) + "\nОтветить через чат: id" + str(event.user_id), vk_session, event.raw[1])
                        #write_msg(int(event.user_id), u'Ваше сообщение переслано администратору сообщества! ;-)\nОн ответит Вам в ближайшее время.\nВ группе тестируеться бот, просим прощение за неудобства.', vk_session)

                elif event.type == VkEventType.USER_TYPING:
                    print('Печатает ', end='')

                    if event.from_user:
                        print(event.user_id)
                    elif event.from_group:
                        print('администратор группы', event.group_id)

                elif event.type == VkEventType.USER_TYPING_IN_CHAT:
                    print('Печатает ', event.user_id, 'в беседе', event.chat_id)

                elif event.type == VkEventType.USER_ONLINE:
                    print('Пользователь', event.user_id, 'онлайн', event.platform)

                elif event.type == VkEventType.USER_OFFLINE:
                    print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

                else:
                    print(event.type, event.raw[1:])
            except requests.exceptions.ReadTimeout as e:
                print(e)
                time.sleep(10)
            except requests.packages.urllib3.exceptions.ReadTimeoutError as e:
                print(e)
                longpoll.update_longpoll_server()
    except Exception as e:
        print(e)
        time.sleep(10)
        main(longpoll)

if __name__ == '__main__':
    main()