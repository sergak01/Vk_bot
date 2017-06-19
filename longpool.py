# -*- coding: utf-8 -*-
import vk_api
import re
from vk_api.longpoll import VkLongPoll, VkEventType

import settings

def write_msg(user_id, s, vk_session):
    vk_session.method('messages.send', {'user_id':user_id,'message':s})

def main():
    try:
        """ Пример использования longpoll
            https://vk.com/dev/using_longpoll
            https://vk.com/dev/using_longpoll_2
        """

        #login, password = '', ''
        #vk_session = vk_api.VkApi(login, password)
        token = settings.vk_token
        vk_session = vk_api.VkApi(token = token)
        vk_user_session = vk_api.VkApi(token = settings.vk_user_token)
        vk_empty_session = vk_api.VkApi()

        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():

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
                        str(event.user_id) + "\nОтветить через чат: id" + str(event.user_id), vk_session)
                    write_msg(int(event.user_id), u'Ваше сообщение переслано администратору сообщества! ;-)\nОн ответит Вам в ближайшее время.\nВ группе тестируеться бот, просим прощение за неудобства.', vk_session)

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
    except Exception as e:
        print(e)
        main()

if __name__ == '__main__':
    main()