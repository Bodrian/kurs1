import requests
import time
import json
from pprint import pprint

class Vk():
    """Работа с ВК"""

    def __init__(self, token):
        self.token = token

    def photos_get_profile(self, id):
        '''Берем список фото из профиля'''
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id.strip(),
            'album_id': 'profile',
            'extended': True,
            'photo_sizes': True,
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(URL, params=params, timeout=5)
        return res

    def select_best_foto(self, res):
        '''Выбираем фотографии наилучшего качества из профиля'''
        TYPE_TUPLES = ('w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's')  # приоритетное качество фото
        result = []
        for j in range(len(res.json()['response']['items'])):
            size_max = 10
            for i in range(len(res.json()['response']['items'][j]['sizes'])):
                size = res.json()['response']['items'][j]['sizes'][i]['type']
                if size_max > TYPE_TUPLES.index(size):
                    size_max = TYPE_TUPLES.index(size)
                    url_foto = res.json()['response']['items'][j]['sizes'][i]['url']
            dic_res = {
                "file_name": f"{res.json()['response']['items'][j]['likes']['count']}.jpg",
                "size": TYPE_TUPLES[size_max],
                "url": url_foto,
                "date": res.json()['response']['items'][j]['date'],
                "likes": res.json()['response']['items'][j]['likes']['count']
            }
            result.append(dic_res)
        return result

    def rename_file_likes(self, result):
        '''Изменяем имя файла для фото с одинаковым количеством лайков'''
        likes = []
        for like in result:
            likes.append(like['likes'])
        likes_unique = list(set(likes))
        for like in likes_unique:
            likes.remove(like)
        likes = list(set(likes))
        print('Отслеживание процесса: Количество лайков по каждой фото получено')
        # преобразуем время с начала эпохи в дату и добавляем в одинаковое кол-во лайков
        for file_name in result:
            for like in likes:
                if like == file_name['likes']:
                    time_name = time.localtime(file_name["date"])
                    file_name['file_name'] = f'{like} {time_name.tm_mday}.{time_name.tm_mon}.{time_name.tm_year}.jpg'
        return result

    def create_json(self, result, file_path):
        '''Создает JSon в директории с программой'''
        json_tmp = []
        for i in result:
            dic_tmp = {}
            dic_tmp['file_name'] = i['file_name']
            dic_tmp['size'] = i['size']
            json_tmp.append(dic_tmp)
        with open(file_path, 'w') as f:
            json.dump(json_tmp, f)

# def error_request(error):
#     '''Расшифровка ошибок ответа'''
#     i = error // 100
#     if i == 2:
#         print(f'{error} - Запрос отработан успешно')
#     elif i == 4:
#         print(f'{error} - ошибка на стороне клиента')
#     elif i == 5:
#         print(f'{error} - ошибка на стороне сервера')
#     elif i == 3:
#         print(f'{error} - ответ сервера - перенаправление')
#     elif i == 1:
#         print(f'{error} - ответ сервера - информационный')

# if __name__ == '__main__':
#     token = ''
#     id = '1'
#     vk = Vk(token)
#     res = vk.photos_get_profile(id)
#     pprint(res.json())
#     error_request(res.status_code)