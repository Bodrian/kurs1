import json
from pprint import pprint

from yandex import Yandex
from vk import Vk

if __name__ == '__main__':

    def get_token(token_file):
        '''Выдергивает токен из файла'''
        with open(token_file, 'r') as file_object:
            token = file_object.read().strip()
        return token

    file_path = 'filename.json' #имя JSON файла
    #работа с API VK
    id = input('Введите id изучаемой учетки Вконтакте (например Павла Дурова - 1): ')
    token = get_token('token.txt')
    vk = Vk(token)
    res = vk.photos_get_profile(id)
    print('Отслеживание процесса: Данные от ID получены')

    error_test = res.json().get('error') # проверка на приватность
    if error_test != None and error_test.get('error_code') == 30:
        print('Профиль защищен настройками приватности')

    else:
        print('Отслеживание процесса: Профиль не защищен настройками приватности - продолжаю')
        result = vk.select_best_foto(res)
        print(f'Отслеживание процесса: Выбраны {len(result)} фото наилучшего разрешения')
        result = vk.rename_file_likes(result) #если у фото одинаковое кол-во лайков - переименовываем
        print('Отслеживание процесса: Имена файлов для запист на Я-Диск подготовлены')
        vk.create_json(result, file_path) #составляем файл json
        print('Отслеживание процесса: Файл Json создан')

        # далее операции с Я-Диском
        token = get_token('tokenya.txt')
        dir_name = input('Укажите название создаваемой папки: ')
        ya = Yandex(token)
        ya.make_dir(dir_name) #создаем папку
        print('Отслеживание процесса: Папка на Я-Диске создана')
        for i, foto in enumerate(result):        #загружаем файлы на Я-диск
            ya.upload_file_url(dir_name, foto["file_name"], foto['url'])
            print(f'Отслеживание процесса: загружено {i+1} фото из {len(result)}')
        ya.upload_file_path(dir_name, file_path) #загружаем json на Я-Диск
        print('Отслеживание процесса: Файл JSON записан на Я-Диск')
        print('Отслеживание процесса: Задание выполнено')