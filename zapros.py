import requests
import json

url = 'http://localhost:5000/user/register'  # URL сервера Flask

# JSON данные для отправки в POST запросе
data = {
    'username': 'MichaelAndIslam',
    'password': 'MAI123'
}

# Отправка POST запроса
response = requests.post(url, json=data)

# Проверка статус кода ответа
if response.status_code == 201:
    print('Пользователь успешно зарегистрирован!')

else:
    print('Произошла ошибка при регистрации пользователя.\n'
          'Пользователь с таким логином уже существует или не введён логин или пароль!')