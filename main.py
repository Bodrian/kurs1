from yandex import Yandex
from vk import Vk

if __name__ == '__main__':
    tokenvk = ''
    tokenya = ''
    file_path = 'filename.json' #имя JSON файла

    #работа с API VK
    id = input('Введите id изучаемой учетки Вконтакте (например Павла Дурова - 1): ')
    vk = Vk(tokenvk)
    print('Отслеживание процесса: Запрашиваю фото профиля с ID')
    res = vk.photos_get_profile(id)
    if res == 'Error':
        print('Завершение работы')
    else:
        print('Отслеживание процесса: Данные от ID получены')
        result = vk.select_best_foto(res)
        print(f'Отслеживание процесса: Выбраны {len(result)} фото наилучшего разрешения')
        result = vk.rename_file_likes(result) #если у фото одинаковое кол-во лайков - переименовываем
        print('Отслеживание процесса: Имена файлов для записи на Я-Диск подготовлены')
        vk.create_json(result, file_path) #составляем файл json
        print('Отслеживание процесса: Файл Json создан')

        # далее операции с Я-Диском
        dir_name = input('Укажите название создаваемой папки: ')
        ya = Yandex(tokenya)
        print('Отслеживание процесса: Создаем папку на Я-Диске')
        ya.make_dir(dir_name) #создаем папку
        for i, foto in enumerate(result):        #загружаем файлы на Я-диск
            print(f'Отслеживание процесса: Загружаю {i + 1} фото из {len(result)}')
            ya.upload_file_url(dir_name, foto["file_name"], foto['url'])
        print('Отслеживание процесса: Записываю файл JSON на Я-Диск')
        ya.upload_file_path(dir_name, file_path) #загружаем json на Я-Диск
        print('Отслеживание процесса: Программа выполнена')