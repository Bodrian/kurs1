import time
import requests
from pprint import pprint

if __name__ == '__main__':

    def get_token(token_file):
        '''Выдергивает токен из файла'''
        with open(token_file, 'r') as file_object:
            token = file_object.read().strip()
        return token

    result = []
    token = get_token('token.txt')
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': '1',
        'album_id': 'profile',
        'extended': True,
        'photo_sizes': True,
        'access_token': token,
        'v': '5.131'
    }
    res = requests.get(URL, params=params)
    pprint(res.json())

    error_test = res.json().get('error') # проверка на приватность
    if error_test != None and error_test.get('error_code') == 30:
        print('Профиль защищен настройками приватности')

    else:
        TYPE_TUPLES = ('w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's') # определяем самые качественное фото по типу
        for j in range(len(res.json()['response']['items'])):
            size_max = 10
            for i in range(len(res.json()['response']['items'][j]['sizes'])):
                size = res.json()['response']['items'][j]['sizes'][i]['type']
                if size_max > TYPE_TUPLES.index(size):
                    size_max = TYPE_TUPLES.index(size)
                    url_foto = res.json()['response']['items'][j]['sizes'][i]['url']
            dic_res = {
                "file_name" : f"{res.json()['response']['items'][j]['likes']['count']}.jpg",
                "size" : TYPE_TUPLES[size_max],
                "url" : url_foto,
                "date" : res.json()['response']['items'][j]['date'],
                "likes" : res.json()['response']['items'][j]['likes']['count']
            }
            result.append(dic_res)
        pprint(result)
        # Сравним количество лайков для фото и при необходимости добавим дату загрузки
        likes = [] #ищем одинаковое кол-во лайков
        for like in result:
            likes.append(like['likes'])
        print(likes)
        likes_unique = list(set(likes))
        for like in likes_unique:
            likes.remove(like)
        likes = list(set(likes))
        print(likes)
        # преобразуем время с начала эпохи в дату и добавляем в одинаковое кол-во лайков
        for file_name in result:
            for like in likes:
                if like == file_name['likes']:
                    time_name = time.localtime(file_name["date"])
                    file_name['file_name'] = f'{like} {time_name.tm_mday}.{time_name.tm_mon}.{time_name.tm_year}.jpg'
        pprint(result) #в этом списке все данные для загрузки на Я-Диск

        # далее операции с Я-Диском
        token = get_token('tokenya.txt')
        #создаем папку
        dir_name = input('Укажите название создаваемой папки: ')
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }
        params = {'path': dir_name}

        response = requests.put(url, headers=headers, params=params, timeout=5)
        print(response)

        #загружаем файлы на Я-диск
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for foto in result:
            params = {
                'path': f'/{dir_name}/{foto["file_name"]}',
                'url': foto['url']
            }
            response = requests.post(url, params=params, headers=headers, timeout=5)
            print(response)

        # далее нужно отредактировать json и загрузить его


        #
        # kaka = [2, 4, 5, 4, 7, 8, 2, 6, 7, 2]
        # kiki = list(set(kaka))
        # print(kiki)
        # for k in kiki:
        #     kaka.remove(k)
        # print(kaka)
        # kaka = list(set(kaka))
        # print(kaka)


            # print(url_foto) #ссылка на максимальное фото для скачивания
            # print(TYPE_TUPLES[size_max]) #ссылка на тип - нужно записать в файл
            # print(res.json()['response']['items'][j]['likes']['count']) #число лайков
            # print(res.json()['response']['items'][j]['date']) #дата создания


    # else: #если профиль не приватный - ищем фото наилучшего качества - по длине и высоте не удалось найти фото до 2012 года
    #     for j in range(len(res.json()['response']['items'])):
    #         # определяю максимальное фото
    #         size_max = 0
    #         for i in range(len(res.json()['response']['items'][j]['sizes'])):
    #             #pprint(res.json()['response']['items'][j]['sizes'][i])
    #             size = res.json()['response']['items'][j]['sizes'][i]['height'] + res.json()['response']['items'][j]['sizes'][i]['width']
    #             #print(size)
    #             if size_max < size:
    #                 size_max = size
    #                 url_foto = res.json()['response']['items'][j]['sizes'][i]['url']
    #                 type_img = res.json()['response']['items'][j]['sizes'][i]['type']
    #         print(size_max) #строка проверки мксимального размера
    #         print(url_foto) #ссылка на максимальное фото для скачивания
    #         print(type_img) #ссылка на тип - нужно записать в файл
    #         print(res.json()['response']['items'][j]['likes']['count']) #число лайков
    #         print(res.json()['response']['items'][j]['date']) #дата создания

        ##### Проблема до 2012 года у фото нет параметров длины и ширины, думаю нужно сделать перебор по списку значений Type по величине try и expect.