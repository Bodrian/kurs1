def error_request(error):
    '''Расшифровка ошибок ответа'''
    i = error // 100
    if error == 200:
        print(f'{error} - Запрос отработан успешно - ОК')
    elif error == 201:
        print(f'{error} - Запрос отработан успешно - создано')
    elif error == 202:
        print(f'{error} - Запрос отработан успешно - принято')
    elif i == 2:
        print(f'{error} - Запрос отработан успешно')
    elif i == 4:
        print(f'{error} - ошибка на стороне клиента')
    elif i == 5:
        print(f'{error} - ошибка на стороне сервера')
    elif i == 3:
        print(f'{error} - ответ сервера - перенаправление')
    elif i == 1:
        print(f'{error} - ответ сервера - информационный')