import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from database.database import DB, DSN
from vk.vk import send_img, send_msg, get_user_info, search_user, get_photos


token_user = ''
token_group = ''
vk = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(vk)


def logic(sex):
    sex_r = 0
    if sex == 2:
        sex_r = 1
    if sex == 1:
        sex_r = 2
    age_from = 18
    age_to = age + 5
    return sex_r, age_from, age_to


if __name__ == '__main__':
    exit = False
    for event in longpoll.listen():
        if exit:
            break
        else:
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    age, sex, relation, city, user_name = get_user_info(event.user_id)
                    send_msg(event.user_id,
                              f"{user_name}, Вас приветствует бот VKinder, который поможет найти Вашу вторую половинку,"
                              f" основываясь на Вашем возрасте ({age}), городе проживания и некоторых других "
                              f"параметрах."
                              f"\nБот направит популярные фото пользователей, а Вы на их основании можете принять "
                              f"решение, хотите ли познакомиться с данным человеком поближе, либо хотите перейти к "
                              f"следующей анкете.")
                    sex_r, age_from, age_to = logic(sex)
                    response = search_user(token_user, age_from, age_to, sex_r, [1, 6], city)
                    for person in response.json()['response']['items']:
                        if exit:
                            break
                        else:
                            if not person['is_closed'] and person['id'] not in DB(DSN).read_from_blacklist():
                                url_list = get_photos(token_user, person['id'])
                                send_img(event.user_id, 'Это ' + str(person['first_name'] + ' ' + person['last_name']
                                         + f'\nЕсли пользователь понравился, напишите:\n\n+\n\nесли не понравился, '
                                           f'напишите:\n\n-\n\n для выхода напишите:\n\nq'), url_list)
                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW:
                                        if event.to_me:
                                            request = event.text
                                            if request.lower() == "+":
                                                send_msg(event.user_id, f"Вы можете ознакомиться с анкетой пользователя"
                                                                        f" более подробно и написать сообщение: "
                                                                        f"vk.com/id{person['id']}\n\n-----")
                                                DB(DSN).add_to_blacklist(person['id'], True)
                                                break
                                            elif request.lower() == "q":
                                                exit = True
                                                break
                                            else:
                                                DB(DSN).add_to_blacklist(person['id'], False)
                                                break
