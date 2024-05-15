# Импорт необходимых модулей
from flask import Flask, request, jsonify
import bcrypt
from datetime import datetime
from flask_sslify import SSLify
import json
import os

# Инициализация приложения Flask
app = Flask(__name__)
sslify = SSLify(app)
users_file = 'users.json'
users = []  # список зарегистрированных пользователей


# Загрузка данных о пользователях из файла
def load_users():
    global users
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            users = json.load(file)


# Сохранение данных о пользователях в файл
def save_users():
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)


# Обработчик запроса на регистрацию пользователя
@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        print("Пользователь не ввёл логин или пароль!")
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    if any(user.get('username') == username for user in users):
        print("Пользователь с таким логином уже существует!")
        return jsonify({'error': 'Username already exists'}), 400

    # Хеширование пароля пользователя
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Получение текущей даты в формате ГГГГ-ММ-ДД
    registration_date = datetime.now().strftime('%Y-%m-%d')

    # Создание информации о пользователе
    user_info = {'username': username, 'password_hash': password_hash.decode('utf-8'),
                 'registration_date': registration_date}

    # Добавление информации о пользователе в список пользователей и сохранение
    users.append(user_info)
    save_users()

    print("Зарегистрирован пользователь:")
    print(user_info)

    return jsonify({'message': 'User registered successfully'}), 201


# Загрузка данных о пользователях и запуск приложения Flask
if __name__ == '__main__':
    load_users()
    app.run(debug=True, threaded=True)