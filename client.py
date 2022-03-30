import json
# from platform import java_ver
import socket
from os import urandom
# from numpy import product
import binascii
# from flask_bcrypt import Bcrypt
# import imp

soc = socket.socket()


def client_connect():

    soc.connect(('127.0.0.1', 8000))

    query_client = {}

    while 1:

        print()
        if (query_client == {}) or not ('token' in query_client):
            print("Авторизиризация")
            task = 0

        else:
            print("Выберите действие:")
            print("1-Просмотреть список заказов")
            print("2-Просмотреть данные заказа")
            print("3-Изменить комментарий к заказу")
            print("4-Изменить статус заказа")
            print("5-Посмотреть содержимое заказа")
            print("6-Изменить личный профиль")
            print("7-Поменять пароль")
            print("8-Выйти из личного кабинета")

            task = int(input())

        # soc.sendall(bytes(task,'UTF-8'))
        menu_dict = {
            0: ['auth', author],
            1: ['all_orders', all_orders],
            2: ['get_order', get_order],
            3: ['edit_note', edit_note],
            4: ['edit_status', edit_status],
            5: ['order_content', order_content],
            6: ['edit_profile', edit_profile],
            7: ['edit_password', edit_password],
            8: ['out', out]
        }

        try:
            md = menu_dict.get(task)
            query_client["command"] = md[0]

            query_client = md[1](query_client)
        except:
            if query_client["command"] != 'auth':
                print('Введите команду правильно')
            else:
                print('Неправильный логин или пароль')


def out(query_client):
    print(query_client)
    query_client = {}

    return query_client


def print_order(order):

    print('Id курьера: ',  order['courier_id'])
    print('Id флориста: ',  order['florist_id'])
    print('Id клиента: ', order['client_id'])
    print('Адрес: ',  order['address'])
    print('Дата заказа: ',  order['date_order'])
    print('Дата доставки: ',  order['date_delivery'])
    print('Дата оплаты: ',  order['date_pay'])
    print('Сумма заказа: ',  order['sum'])
    print('Статус заказа: ',  status_order(order['status_order']))
    print('Примечание: ',  order['note'])


def send_get(query_client):
    json_client = json.dumps(query_client)
    soc.sendall(bytes(json_client, 'UTF-8'))

    query_client = soc.recv(1024).decode()
    json_client = json.loads(query_client)
    return json_client


def status_order(json_client):
    if (json_client == 0):
        status_ord = 'Принят'
    else:
        status_ord = 'Доставлен'
    return status_ord


def show(json_client):
    if (json_client == 0):
        status_ord = 'Скрыто'
    else:
        status_ord = 'Не скрыто'
    return status_ord


def author(query_client):
    print(query_client)
    data = {}
    print('Введите номер телефона')
    data['phone'] = input()
    print('Введите пароль')
    data['password'] = input()

    query_client['data'] = data
    json_client = send_get(query_client)
    query_client["i_key"] = binascii.hexlify(urandom(20)).decode()
    print()
    print('Добро пожаловать,',
          json_client['data']['surname'], json_client['data']['name'])
    query_client["token"] = json_client['data']['token']
    print(query_client)

    return query_client


def get_order(query_client):
    print('Введите id заказа')
    task_order = input()
    task_order = int(task_order)
    data = {}
    data['id'] = task_order
    query_client['data'] = data
    json_client = send_get(query_client)
    print_order(json_client['data'])

    return query_client


def all_orders(query_client):

    json_client = send_get(query_client)

    for order in json_client['data']:
        print('Id заказа:',  order['id'])

        print_order(order)
        print()
    return query_client


def edit_note(query_client):
    data = {}

    print('Введите id заказа')
    data['id'] = input()
    print("Введите примечание")
    data['note'] = input()

    query_client['data'] = data

    json_client = send_get(query_client)
    print('Примечание заказа №',
          json_client['data']['id'], 'успешно изменено')
    return json_client


def edit_status(query_client):
    data = {}

    print('Введите id заказа')
    data['id'] = input()
    print("Введите статус")
    print("0-Принят")
    print("1-Доставлен")
    data['status_order'] = input()
    query_client['data'] = data

    json_client = send_get(query_client)
    print('Статус заказа №',
          json_client['data']['id'], 'успешно изменен')
    return json_client


def order_content(query_client):
    data = {}
    print('Введите id заказа')
    task_order = input()
    task_order = int(task_order)
    data = {}
    data['id_order'] = task_order
    query_client['data'] = data

    json_client = send_get(query_client)
    for product in json_client['data']:
        print_product(product)
    return json_client


def print_product(product):
    print()
    print('Id товара:',  product['id'])
    print('Название товара:',  product['name'])
    print('Категория товара:',  product['subcategory_id'])
    print('Описание товара:',  product['description'])
    print('Id поставщика:',  product['supplier_id'])
    print('Цена:',  product['price'])
    print('Отображение:',  show(product['show']))
    print('Артикул товара:',  product['article'])


def edit_profile(query_client):
    data = {}

    print('Введите имя')
    data['name'] = input()

    query_client['data'] = data

    json_client = send_get(query_client)
    print("Ваши данные успешно изменены")
    return json_client


def edit_password(query_client):
    data = {}
    print('Введите старый пароль')
    data['old_password'] = input()
    print('Введите новый пароль')
    data['new_password'] = input()
    print('Подтвердите новый пароль')
    data['new_password1'] = input()
    query_client['data'] = data

    json_client = send_get(query_client)
    print("Ваш пароль успешно изменен")
    return json_client


# client_connect()
