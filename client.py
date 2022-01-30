import json
from platform import java_ver
import socket
from os import urandom
from numpy import product
import binascii

# from server import Order


def client_connect():
    soc = socket.socket()

    soc.connect(('127.0.0.1', 8000))

    auth = 0
    query_client = {}

    while 1:

        print()
        if auth == 0:
            print("Авторизиризация")
            task = "1"

        if auth == 1:
            print("Выберите действие:")
            print("2-Просмотреть список заказов")
            print("3-Просмотреть данные заказа")
            print("4-Изменить комментарий к заказу")
            print("5-Изменить статус заказа")
            print("6-Посмотреть содержимое заказа")
            print("7-Изменить личный профиль")
            print("8-Поменять пароль")
            print("9-Выйти из личного кабинета")

            task = input()

        # soc.sendall(bytes(task,'UTF-8'))

        query_client["i_key"] = binascii.hexlify(urandom(20)).decode()

        # if task=="1":
        #     query_client["data"]=add_client()
        # if json_client["status"]==True:
        #     print("yes")

        # if task=="2":
        #     # query_client["task"]=task
        #     # query_client["i_key"]="987654321"
        #     # query_client["token"]=""
        #     # query_client["data"]=all_orders()

        if task == "1":
            query_client["command"] = "auth"

            query_client["data"] = author()

        if task == "2":

            query_client["command"] = "all_orders"

        if task == "3":
            query_client["command"] = "get_order"

            query_client["data"] = get_order()

        if task == "4":
            query_client["command"] = "edit_note"

            query_client["data"] = edit(task)

        if task == "5":
            query_client["command"] = "edit_status"

            query_client["data"] = edit(task)

        if task == "6":
            query_client["command"] = "order_content"

            query_client["data"] = order_content()

        if task == "7":
            query_client["command"] = "edit_profile"

            query_client["data"] = edit_profile()

        if task == "8":
            query_client["command"] = "edit_password"

            query_client["data"] = edit_password()

        json_client = convertjson(query_client, soc)
        exc(query_client["command"], json_client)
        if task == '1':
            try:
                print('Добро пожаловать,',
                      json_client['data']['surname'], json_client['data']['name'])
                auth = 1
                query_client["token"] = json_client['data']['token']
            except:
                print()

        if task == "9":
            auth = 0

        if not task.isdigit() or int(task) > 9:
            print("error")

            # if task=="1":
            #     print(json_client)

            #     print('Вы успешно зарегистрировались! Ваш id: ', json_client['id'])


def exc(command, json_client):
    try:

        if (command == 'all_orders'):
            for order in json_client['data']:
                print('Id заказа:',  order['id'])

                print_order(order)
        if (command == 'get_order'):
            print_order(json_client['data'])
        if (command == 'edit_note'):
            print('Примечание заказа №',
                  json_client['data']['id'], 'успешно изменено')
        if (command == 'edit_note'):
            print('Примечание заказа №',
                  json_client['data']['id'], 'успешно изменено')
        if (command == 'edit_status'):
            print('Статус заказа №',
                  json_client['data']['id'], 'успешно изменен')
        if (command == 'order_content'):
            for product in json_client['data']:
                print_product(product)
        if (command == 'edit_profile'):
            print("Ваши данные успешно изменены")
        if (command == 'edit_password'):
            print("Пароль успешно изменен")
        if json_client['data'] == None:
            print('error')

    except:

        print('error')


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


def convertjson(query_client, soc):
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

# def add_client():
#     data={}


#     print("Введите имя")
#     data ['name']=input()
#     print("Введите номер телефона")
#     data ['phone']=input()

#     print("Введите дату рождения в формате ГГГГ-ММ-ДД")

#     data ['birthday']=input()
#     return data


def author():
    data = {}
    print('Введите номер телефона')
    data['phone'] = input()
    print('Введите пароль')
    data['password'] = input()
    return data


def get_order():
    print('Введите id заказа')
    task_order = input()
    task_order = int(task_order)
    data = {}
    data['id'] = task_order

    return data


def edit(task):
    data = {}

    print('Введите id заказа')
    data['id'] = input()
    if (task == "4"):
        print("Введите примечание")
        data['note'] = input()
    else:
        print("Введите статус")
        print("0-Принят")
        print("1-Доставлен")
        data['status_order'] = input()
    return data


def order_content():
    data = {}
    print('Введите id заказа')
    task_order = input()
    task_order = int(task_order)
    data = {}
    data['id_order'] = task_order

    return data


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


def edit_profile():
    data = {}

    print('Введите имя')
    data['name'] = input()

    return data


def edit_password():
    data = {}
    print('Введите старый пароль')
    data['old_password'] = input()
    print('Введите новый пароль')
    data['new_password'] = input()
    print('Подтвердите новый пароль')
    data['new_password1'] = input()
    return data


client_connect()
