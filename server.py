#from concurrent.futures.process import _python_exit
#from email.header import decode_header
from http import client
import json
import sqlite3


from tokenize import Double
from traceback import print_tb
from datetime import datetime, date
from numpy import product

#from pydoc import cli
#import re
#from turtle import color
from sqlalchemy import ForeignKey, create_engine, Integer, String, Boolean, Date, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
import socket


import logging

logging.basicConfig(filename='log.log',
                    format='%(asctime)s - %(message)s', level=logging.INFO)


e = create_engine("sqlite:///mydatabase.db")

# e = create_engine("postgresql+psycopg2://postgres:123@localhost/postgres")

Base = declarative_base()


s = Session(bind=e)


class User(Base):
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

    def add_client(client):

        # data=client["data"]
        c = User()
        c.name = ["name"]
        c.phone = ["phone"]
        c.birthday = ["birthday"]

        c.token = "234567sfdghgh3546"

        s.add(c)
        s.commit()

        return True

    def auth(data):

        user = s.query(User).filter(User.phone == data['phone']).first()

        if user.password == data['password']:
            data['id'] = user.id
            data['surname'] = user.surname
            data['name'] = user.name
            data['patronymic'] = user.patronymic
            data['birthday'] = str(user.birthday)
            data['token'] = user.token
            return data

    def edit_profile(data):
        courier = s.query(User).filter(User.token == data['token']).first()
        courier.name = data['data']['name']

        s.add(courier)
        s.commit()

        return data['data']

    def edit_password(data):
        courier = s.query(User).filter(User.token == data['token']).first()
        if (courier.password == data['data']['old_password'] and data['data']['new_password'] == data['data']['new_password1']):
            courier.password = data['data']['new_password']
            s.add(courier)
            s.commit()

            return data['data']


class Order(Base):
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

    def all_orders(data):
        courier = s.query(User).filter(User.token == data['token']).first()
        orders = courier.order
        new_orders = []  # [{} {} {}]
        for order in orders:
            data = {}
            data = Order.print_order(order, data)

            new_orders.append(data)
        data = new_orders
        return data

    def get_order(data):
        courier = s.query(User).filter(User.token == data['token']).first()

        order = s.query(Order).get(data['data']['id'])
        if order in courier.order:
            data = Order.print_order(order, data['data'])

            return data

    def print_order(order, a):

        a['id'] = order.id
        a['courier_id'] = order.courier_id
        a['florist_id'] = order.florist_id
        a['client_id'] = order.client_id
        a['address'] = order.address
        a['date_order'] = str(order.date_order)
        a['date_delivery'] = str(order.date_delivery)
        a['date_pay'] = str(order.date_pay)
        a['sum'] = order.sum
        a['status_order'] = order.status_order
        a['note'] = order.note
        return a

    def edit_note(data):
        courier = s.query(User).filter(User.token == data['token']).first()
        order = s.query(Order).get(data['data']['id'])

        if order in courier.order:
            order.note = data['data']['note']
            s.add(order)
            s.commit()

            return data['data']

    def edit_status(data):
        courier = s.query(User).filter(User.token == data['token']).first()
        order = s.query(Order).get(data['data']['id'])
        if order in courier.order:
            order.status_order = data['data']['status_order']
            s.add(order)
            s.commit()

            return data['data']


class Product(Base):
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

    __tablename__ = 'ordercontent'
    id = Column(Integer, primary_key=True)

    order_id = Column(Integer,  ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quanity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="content_order")
    product = relationship("Product", back_populates="content_product")

    def order_content(data):
        courier = s.query(User).filter(User.token == data['token']).first()

        order = s.query(Order).get(data['data']['id_order'])
        if order in courier.order:

            order_c = order.content_order
            new_orders = []  # [{} {} {}]
            for product in order_c:
                data = {}
                product_ = s.query(Product).get(product.product_id)
                data['id'] = product_.id
                data['name'] = product_.name
                data['subcategory_id'] = product_.subcategory_id
                data['description'] = product_.description
                data['supplier_id'] = product_.supplier_id
                data['price'] = product_.price
                data['show'] = product_.show
                data['article'] = product_.article
                new_orders.append(data)
            data = new_orders
            return(data)


# Base.metadata.create_all(e)


def server_connect():

    ADDRESS = '127.0.0.1'
    PORT = 8000

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((ADDRESS, PORT))

    soc.listen(1)

    print("work")

    while 1:
        connection, address = soc.accept()
        print('Клиент подключен', address)
        logging.warning('Клиент подключен' + str(address))

        while 1:
            query_client = connection.recv(1024)
            decode_query = query_client.decode()

            json_query = json.loads(decode_query)
            print(json_query)

            if json_query["command"] == 'auth':
                json_query['data'] = User.auth(json_query['data'])

            if json_query['command'] == 'all_orders':
                json_query['data'] = Order.all_orders(json_query)

            if json_query['command'] == 'get_order':

                json_query['data'] = Order.get_order(
                    json_query)

            if json_query['command'] == 'edit_note':
                json_query['data'] = Order.edit_note(
                    json_query)

            if json_query['command'] == 'edit_status':
                json_query['data'] = Order.edit_status(
                    json_query)

            if json_query['command'] == 'order_content':
                json_query['data'] = OrderContent.order_content(
                    json_query)
            if json_query['command'] == 'edit_profile':
                json_query['data'] = User.edit_profile(
                    json_query)
            if json_query['command'] == 'edit_password':
                json_query['data'] = User.edit_password(
                    json_query)

            connection.sendall(bytes(json.dumps(json_query), 'UTF-8'))

            print(json_query)


server_connect()
