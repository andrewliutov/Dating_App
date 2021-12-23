import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from database.database import Database
from vk.vk import Vkontakte
from settings import TOKEN_USER, TOKEN_GROUP, DSN


vk = Vkontakte()
db = Database(DSN)

vka = vk_api.VkApi(token=TOKEN_GROUP)
longpoll = VkLongPoll(vka)


def main():
    exit = False
    for event in longpoll.listen():
        if exit:
            break
        else:
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    age, sex, relation, city, user_name = vk.get_user_info(event.user_id)
                    vk.send_msg(event.user_id,
                              f'{user_name}, Вас приветствует бот VKinder, который поможет найти Вашу вторую половинку,'
                              f' основываясь на Вашем возрасте ({age}), городе проживания и некоторых других '
                              f'параметрах.'
                              f'\nБот направит популярные фото пользователей, а Вы на их основании можете принять '
                              f'решение, хотите ли познакомиться с данным человеком поближе, либо хотите перейти к '
                              f'следующей анкете.')
                    if sex == 0:
                        vk.send_msg(event.user_id, 'В анкете не указан Ваш пол, укажите его сейчас, пожалуйста. Если Вы'
                                                   'женщина - введите 1, если мужчина  - 2')
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request = event.text
                                    if request.lower() == '1':
                                        sex = 1
                                    if request.lower() == '2':
                                        sex = 2
                    sex_to_search, age_from, age_to = vk.get_age_sex(age, sex)
                    response = vk.search_user(TOKEN_USER, age_from, age_to, sex_to_search, [1, 6], city)
                    for person in response.json()['response']['items']:
                        if exit:
                            break
                        else:
                            if not person['is_closed'] and person['id'] not in db.read_from_blacklist():
                                url_list = vk.get_photos(TOKEN_USER, person['id'])
                                vk.send_img(event.user_id, 'Это ' + str(person['first_name'] + ' ' + person['last_name']
                                         + f'\nЕсли пользователь понравился, напишите:\n\n+\n\nесли не понравился, '
                                           f'напишите:\n\n-\n\n для выхода напишите:\n\nq'), url_list)
                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW:
                                        if event.to_me:
                                            request = event.text
                                            if request.lower() == '+':
                                                vk.send_msg(event.user_id, f"Вы можете ознакомиться с анкетой "
                                                                           f"пользователя более подробно и написать "
                                                                           f"сообщение: vk.com/id{person['id']}\n\n")
                                                db.add_to_blacklist(person['id'], True)
                                                break
                                            elif request.lower() == '-':
                                                db.add_to_blacklist(person['id'], False)
                                                break
                                            elif request.lower() == 'q':
                                                vk.send_msg(event.user_id, f'Бот завершил поиск анкет, до свидания!\n'
                                                                           f'Если захотите воспользоваться поиском еще '
                                                                           f'раз - отправьте боту любое сообщение.')
                                                exit = True
                                                break


if __name__ == '__main__':
    main()
