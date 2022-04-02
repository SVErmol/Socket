# from re import X
# import string
# from sys import exit
# from http import client
import json
import sqlite3
import win32api
from winerror import ERROR_ALREADY_EXISTS
import win32event
import yaml
# from tokenize import Double
# from traceback import print_tb
from datetime import datetime, date
from numpy import product
# import threading

from sqlalchemy import ForeignKey, create_engine, Integer, String, Boolean, Date, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
import socket
import hashlib
from exceptions import *

import logging
from memcache import *
from pymemcache.client import base

with open('settings') as conf:
    # config = configparser.ConfigParser()
    conf = yaml.safe_load(conf)
salt = conf['salt']

file_log = logging.FileHandler('log.log')
console_log = logging.StreamHandler()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%d.%b.%Y %H:%M:%S",
    handlers=(file_log, console_log))
log = logging.getLogger('server')

# e = create_engine("sqlite:///mydatabase.db")

# e = create_engine("postgresql+psycopg2://postgres:123@localhost/postgres")

Base = declarative_base()


client = conf['client']

# client.set('some_key', 'some value')

# client.get('some_key') # 'some value'

s = Session(bind=create_engine(conf['engine_sqlite']))


def object_to_dict(ob):
    """
    Метод для преобразования объекта в словарь
    :param ob: объект
    :return: словарь
    """
    return {x.name: (str(getattr(ob, x.name)))
            for x in ob.__table__.columns
            }


class User(Base):
    """
    Класс пользователя

    id-id пользователя
    surname-фамилия пользователя
    name-имя пользователя
    patronymic-отчество пользователя
    phone-номер телефона
    birthday-дата рождения
    password-пароль
    token-токен
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    patronymic = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)
    birthday = Column(Date, nullable=False)
    password = Column(String(250), nullable=False)
    token = Column(String(250), nullable=False)

    order = relationship("Order", back_populates='courier')



    def auth(data):
        """
        Метод для авторизации пользователя
         :param data: словарь с номером телефона и паролем
        :return: словарь с информацией о пользователе
        """
        user = s.query(User).filter(User.phone == data['phone']).first()
        salt_ = hashlib.sha256(
            data['password'].encode()+salt.encode()).hexdigest()
        if user.password == salt_:
            
            data = object_to_dict(user)
            data['password']=user.password
            return data

    def edit_profile(data, courier):
        """

        :param courier: объект типа User
                data: словарь с информацией, которую хочет изменить пользователь
        :return: data: словарь с измененной информацией
        """
        courier.name = data['name']

        s.add(courier)
        s.commit()

        return data

    def edit_password(data, courier):
        """

              :param courier: объект типа User
                      data: словарь с новым и старым паролем
              :return: data: словарь с измененным паролем
              """
        data['old_password'] = hashlib.sha256(
            data['old_password'].encode() + salt.encode()).hexdigest()
        data['new_password1'] = hashlib.sha256(
            data['new_password1'].encode() + salt.encode()).hexdigest()
        data['new_password'] = hashlib.sha256(
            data['new_password'].encode() + salt.encode()).hexdigest()
        if (courier.password == data['old_password'] and data['new_password'] == data['new_password1']):

            courier.password =  data['new_password']
            s.add(courier)
            s.commit()
            return data


class Order(Base):
    """
    Класс заказа

    id-id заказа
    courier_id-id курьера
    florist_id-id флориста
    client_id-id клиента
    address-адрес заказа
    date_order-дата заказа
    date_delivery-дата доставки
    date_pay-дата оплаты
    sum-сумма оплаты
    status_order-статус заказа
    note-комментарий

    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    florist_id = Column(Integer, nullable=True)
    client_id = Column(Integer, nullable=True)
    address = Column(String(250), nullable=False)
    date_order = Column(Date, nullable=False)
    date_delivery = Column(Date, nullable=False)
    date_pay = Column(Date, nullable=False)
    sum = Column(Integer, nullable=False)
    status_order = Column(Integer, nullable=False)
    note = Column(String(250), nullable=False)

    courier = relationship("User", back_populates="order")

    content_order = relationship("OrderContent", back_populates='order')

    def all_orders(data, courier):
        """

          :param courier: объект типа User
                      data: словарь с данными
        :return: data: словарь с информацией о заказаз курьера
        """
        orders = courier.order
        new_orders = []  # [{} {} {}]
        for order in orders:
            data = object_to_dict(order)
            # data = Order.print_order(order, data)

            new_orders.append(data)
        data = new_orders
        return data

    def get_order(data, courier):
        """

               :param courier: объект типа User
                           data: словарь с данными о номере заказа
             :return: data: словарь с информацией о контретном заказе
             """
        order = s.query(Order).get(data['id'])
        if order in courier.order:
            data = object_to_dict(order)

            return data

    def edit_note(data, courier):
        """

                    :param courier: объект типа User
                                data: словарь с данными о номере заказа и комментарии
                  :return: data: словарь с информацией измененного заказа
                  """
        order = s.query(Order).get(data['id'])

        if order in courier.order:
            order.note = data['note']
            s.add(order)
            s.commit()


            return data

    def edit_status(data, courier):
        """

                         :param courier: объект типа User
                                     data: словарь с данными о номере заказа и статусе
                       :return: data: словарь с информацией измененного заказа
                       """
        order = s.query(Order).get(data['id'])
        if order in courier.order:
            order.status_order = data['status_order']
            s.add(order)
            s.commit()

            return data


class Product(Base):
    """
     Класс товара

     id-id товара
     name-название товара
     subcategory_id-id категории
     photos-фото
     description-описание
     supplier_id-id поставщика
     price-цена
     show-скрывать/показывать
     article-артикул

     """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    subcategory_id = Column(Integer, nullable=False)
    photos = Column(String(250), nullable=True)
    description = Column(String(250), nullable=False)
    supplier_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    show = Column(Integer, nullable=False)
    article = Column(Integer, nullable=False)

    content_product = relationship("OrderContent", back_populates='product')


class OrderContent(Base):
    """
     Класс содержимого заказа

     id-id
     order_id-id
     product_id-id товара
     quanity-количество


     """
    __tablename__ = 'ordercontent'
    id = Column(Integer, primary_key=True)

    order_id = Column(Integer,  ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quanity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="content_order")
    product = relationship("Product", back_populates="content_product")

    def order_content(data, courier):
        """

         :param courier: объект типа User
                                     data: словарь с данными о номере заказа
                       :return: data: словарь с информацией содержимого заказа
        """
        order = s.query(Order).get(data['id_order'])
        if order in courier.order:

            order_c = order.content_order
            new_orders = []  # [{} {} {}]
            for product in order_c:
                data = {}
                product_ = s.query(Product).get(product.product_id)
                data = object_to_dict(product_)
                new_orders.append(data)
            data = new_orders

            return(data)


# Base.metadata.create_all(e)


def server_connect():

    # ADDRESS = '127.0.0.1'
    # PORT = 8000
    port = conf['port']
    address = conf['address']
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((address, port))

    soc.listen(1)

    log.info('Work:'+str(address))
    menu_dict = {
        'auth': User.auth,
        'all_orders': Order.all_orders,
        'get_order': Order.get_order,
        'edit_note': Order.edit_note,
        'edit_status': Order.edit_status,
        'order_content': OrderContent.order_content,
        'edit_profile': User.edit_profile,
        'edit_password': User.edit_password
    }
    while 1:
        connection, address = soc.accept()
        print('client connection', address)
        logging.warning('client connection' + str(address))

        while 1:
            try:
                query_client = connection.recv(1024)
                decode_query = query_client.decode()

                json_query = json.loads(decode_query)
                print(json_query)
            except:
                log.error('Error!')

            if not json_query:
                log.info('Disconnected:' + str(address))
                break
            try:
                com = json_query['command']
                if com == 'auth':
                    json_query['data'] = menu_dict.get(
                        com)(json_query['data'])
                    print(json_query)

                else:
                    courier = s.query(User).filter(
                        User.token == json_query['token']).first()
                    json_query['data'] = menu_dict.get(
                        com)(json_query['data'], courier)
            except NotFoundError as er:
                json_query['message'] = er.message
                log.warning('Not Found!')
            except InternalServerError as er:
                json_query['message'] = er.message
            except ErrorUnauthorized as er:
                json_query['message'] = er.message
                log.error('Unauthorized Error!')
            try:
                connection.sendall(bytes(json.dumps(json_query), 'UTF-8'))
            except:
                log.error('Sending Error!')
            print(json_query)


class single_example:
    def __init__(self):
        self.mutex_name = "testmutex_{b5123b4b-e59c-4ec7-a912-51be8ebd5819}"
        self.mutex = win32event.CreateMutex(None, 1, self.mutex_name)
        self.last_error = win32api.GetLastError()

    def already_working(self):
        return (self.last_error == ERROR_ALREADY_EXISTS)


app = single_example()
if app.already_working():
    print("Server is running")
    exit(0)
server_connect()