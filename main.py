import time
import requests
import json

if __name__ == '__main__':

    def get_token(token_file):
        '''Выдергивает токен из файла'''
        with open(token_file, 'r') as file_object:
            token = file_object.read().strip()
        return token

    result = []
    token = get_token('token.txt')
    URL = 'https://api.vk.com/method/photos.get'
    id = input('Введите id изучаемой учетки Вконтакте (например Павла Дурова - 1): ')
    params = {
        'owner_id': id.strip(),
        'album_id': 'profile',
        'extended': True,
        'photo_sizes': True,
        'access_token': token,
        'v': '5.131'
    }
    res = requests.get(URL, params=params)
    print('Отслеживание процесса: Данные от ID получены')

    error_test = res.json().get('error') # проверка на приватность
    if error_test != None and error_test.get('error_code') == 30:
        print('Профиль защищен настройками приватности')

    else:
        print('Отслеживание процесса: Профиль не защищен настройками приватности - продолжаю')
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
        print(f'Отслеживание процесса: Выбраны {len(result)} фото наилучшего разрешения')
        # Сравним количество лайков для фото и при необходимости добавим дату загрузки
        likes = [] #ищем одинаковое кол-во лайков
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
        #pprint(result) #в этом списке все данные для загрузки на Я-Диск
        print('Отслеживание процесса: Имена файлов для запист на Я-Диск подготовлены')

        #составляем файл json
        json_tmp = []
        for i in result:
            dic_tmp = {}
            dic_tmp['file_name'] = i['file_name']
            dic_tmp['size'] = i['size']
            json_tmp.append(dic_tmp)
        file_path = 'filename.json'
        with open(file_path, 'w') as f:
            json.dump(json_tmp, f)
        print('Отслеживание процесса: Файл Json создан')

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
        print('Отслеживание процесса: Папка на Я-Диске создана')

        #загружаем файлы на Я-диск
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for i, foto in enumerate(result):
            params = {
                'path': f'/{dir_name}/{foto["file_name"]}',
                'url': foto['url']
            }
            response = requests.post(url, params=params, headers=headers, timeout=5)
            print(f'Отслеживание процесса: загружено {i+1} фото из {len(result)}')

        #загружаем json на Я-Диск
        params = {
            'path': f'/{dir_name}/{file_path}',
            'overwrite': 'true'
        }
        response = requests.get(url, headers=headers, params=params, timeout=5)
        dic = response.json()
        response = requests.put(dic['href'], data=open(file_path, 'rb'), headers=headers, timeout=5)
        print('Отслеживание процесса: Файл JSON записан на Я-Диск')
        print('Отслеживание процесса: Задание выполнено')