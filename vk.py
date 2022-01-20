import requests
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