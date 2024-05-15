from flask import Flask, request, jsonify
import bcrypt
from datetime import datetime
from flask_sslify import SSLify
import json
import os

app = Flask(__name__)
sslify = SSLify(app)
users_file = 'users.json'
users = []  # список зарегистрированных пользователей

def load_users():
    global users
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            users = json.load(file)

def save_users():
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)


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

    