import requests

class Yandex():
    """Работа с Я-диском"""

    def __init__(self, token):
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def make_dir(self, dir_name):
        """Создает директорию на Я-Диксе"""
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': dir_name}
        response = requests.put(url, headers=self.headers, params=params, timeout=5)

    def upload_file_url(self, dir_name, file_name, url_file):
        """Загружает файл с URL в заданную папку на Я-Дикс"""
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {
            'path': f'/{dir_name}/{file_name}',
            'url': url_file
        }
        response = requests.post(url, params=params, headers=self.headers, timeout=5)

    def upload_file_path(self, dir_name, file_path):
        """Загружает файл с локального компьютера в заданную папку на Я-Дикс"""
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {
            'path': f'/{dir_name}/{file_path}',
            'overwrite': 'true'
        }
        response = requests.get(url, headers=self.headers, params=params, timeout=5)
        dic = response.json()
        response = requests.put(dic['href'], data=open(file_path, 'rb'), headers=self.headers, timeout=5)