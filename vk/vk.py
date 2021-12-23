from random import randrange
import requests
import vk_api
import datetime
from settings import TOKEN_GROUP


class Vkontakte:
    def __init__(self):
        self.vka = vk_api.VkApi(token=TOKEN_GROUP)
        self.url = 'https://api.vk.com/method/'

    def send_msg(self, user_id, message):
        self.vka.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })

    def send_img(self, user_id, message, photo_link):
        self.vka.method('messages.send',
                  {'peer_id': user_id, 'message': message, 'attachment': photo_link, 'random_id': randrange(10 ** 7)})

    def get_user_info(self, user_id):
        params = {'user_ids': user_id,
                  'access_token': TOKEN_GROUP,
                  'fields': 'city, sex, status, bdate, relation',
                  'v': '5.131',
                  }
        response = requests.get(self.url+'users.get', params=params)
        try:
            bdate = datetime.datetime.strptime(response.json()['response'][0]['bdate'], '%d.%m.%Y')
            age = datetime.datetime.now() - bdate
            age = int(age.total_seconds() // (365.25 * 24 * 60 * 60))
        except:
            age = 0
        try:
            sex = response.json()['response'][0]['sex']
        except:
            sex = 0
        try:
            relation = response.json()['response'][0]['relation']
        except:
            relation = 0
        try:
            city = response.json()['response'][0]['city']['id']
        except:
            city = 0
        user_name = response.json()['response'][0]['first_name']
        return age, sex, relation, city, user_name

    def search_user(self, token_user, age_from, age_to, sex, relation, city):
        params = {'access_token': token_user,
                  'age_from': age_from,
                  'age_to': age_to,
                  'city': city,
                  'sex': sex,
                  'relation': relation,
                  'fields': 'is_closed',
                  'has_photo': 1,
                  'online': 1,
                  'sort': 0,
                  'count': 1000,
                  'v': '5.131',
                  }
        response = requests.get(self.url+'users.search', params=params)
        return response

    def get_photos(self, token_user, user_id):
        photo_dict = {}
        params = {'user_id': user_id,
                  'access_token': token_user,
                  'v': '5.131',
                  'extended': 1,
                  'album_id': 'profile'  # wall, saved, profile
                  }
        response = requests.get(self.url+'photos.get', params=params)
        if response.status_code == 200:
            photo_counter = len(response.json()['response']['items'])
            for i in range(photo_counter):
                photo_id = response.json()['response']['items'][i]['id']
                popularity = (response.json()['response']['items'][i]['likes']['count'] +
                              response.json()['response']['items'][i]['likes']['user_likes'] +
                              response.json()['response']['items'][i]['comments']['count'])
                photo_owner_id = response.json()['response']['items'][i]['owner_id']
                photo_url = f'photo{photo_owner_id}_{photo_id}'
                photo_dict[photo_url] = popularity
        else:
            print('Ошибка:', response)
        sorted_tuple = sorted(photo_dict.items(), key=lambda x: x[1], reverse=True)
        photo_url = []
        photo_counter = len(sorted_tuple)
        if photo_counter > 3:
            photo_counter = 3
        for i in range(photo_counter):
            photo_url.append(sorted_tuple[i][0])
        photo_url = ','.join(photo_url)
        return photo_url

    def get_age_sex(self, age, sex):
        sex_to_search = 0
        female = 1
        male = 2
        if sex == male:
            sex_to_search = female
        if sex == female:
            sex_to_search = male
        age_from = 18
        age_to = age + 5  # expanding search from legal age to user's age + 5 years
        return sex_to_search, age_from, age_to
