import unittest
from unittest.mock import patch, Mock
from server import *
from client import *
import datetime


def test_token():
    return b'23453234567u8765432asdfghhgtrew'


class TestUser(unittest.TestCase):

    def setUp(self):
        self.courier = s.query(User).filter(
            User.token == test_token().decode()).first()

    @patch('binascii.hexlify', side_effect=test_token)
    def test_0_auth(self, mock_token):
        data = {'phone': '123', 'password': '345'}

        result = User.auth(data)
        ex_result = {'id': '1', 'surname': 'Петренко', 'name': 'Татьяна', 'patronymic': 'Григорьевна', 'phone': '123',
                     'birthday': '1999-04-14',
                     'password': '009ddd84de448cad7b31f727504f98347e733975b2b99a17669be7fe6d1ce070',
                     'token': '23453234567u8765432asdfghhgtrew'}
        self.assertEqual(result, ex_result)

    # @patch('builtins.input', return_value='123')
    # #@patch('builtins.input',return_value='345')
    # def test_0_author(self, mock_input):
    #     query_client = {}
    #     # data = {}
    #     # data['phone'] = mock_input()
    #     # data['password'] = mock_input()
    #     result = author(query_client)
    #     ex_result = {'data': {'password': '123', 'phone': '123'}}
    #     self.assertEqual(result, ex_result)

    def test_1_edit_profile(self):
        data = {'name': 'Татьяна'}

        result = User.edit_profile(data, self.courier)
        ex_result = {'name': 'Татьяна'}
        self.assertEqual(result, ex_result)

    def test_7_edit_password(self):
        data = {'old_password': '345', 'new_password': '345', 'new_password1': '345'}

        result = User.edit_password(data, self.courier)
        ex_result = {'old_password': '009ddd84de448cad7b31f727504f98347e733975b2b99a17669be7fe6d1ce070',
                     'new_password': '009ddd84de448cad7b31f727504f98347e733975b2b99a17669be7fe6d1ce070',
                     'new_password1': '009ddd84de448cad7b31f727504f98347e733975b2b99a17669be7fe6d1ce070'}
        self.assertEqual(result, ex_result)


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.courier = s.query(User).filter(
            User.token == test_token().decode()).first()

    def test_2_all_orders(self):
        data = {'phone': '123', 'password': '009ddd84de448cad7b31f727504f98347e733975b2b99a17669be7fe6d1ce070'}
        result = Order.all_orders(data, self.courier)
        ex_result = [{'id': '1', 'courier_id': '1', 'florist_id': '2', 'client_id': '3', 'address': 'Ленина 13',
                      'date_order': '2022-01-01', 'date_delivery': '2022-01-20', 'date_pay': '2022-01-20',
                      'sum': '43534', 'status_order': '0', 'note': 'wow'},
                     {'id': '2', 'courier_id': '1', 'florist_id': '2', 'client_id': '3', 'address': 'Ленина 11',
                      'date_order': '2022-01-28', 'date_delivery': '2022-01-28', 'date_pay': '2022-01-28',
                      'sum': '8756', 'status_order': '1', 'note': 'Быстрее'}]

        self.assertEqual(result, ex_result)

    def test_3_get_order(self):
        data = {'id': 1}
        result = Order.get_order(data, self.courier)
        ex_result = {'id': '1', 'courier_id': '1', 'florist_id': '2', 'client_id': '3', 'address': 'Ленина 13',
                     'date_order': '2022-01-01', 'date_delivery': '2022-01-20', 'date_pay': '2022-01-20',
                     'sum': '43534', 'status_order': '0', 'note': 'wow'}
        self.assertEqual(result, ex_result)

    def test_4_edit_status(self):
        data = {'id': '1', 'status_order': '0'}
        result = Order.edit_status(data, self.courier)
        ex_result = {'id': '1', 'status_order': '0'}
        self.assertEqual(result, ex_result)

    def test_5_edit_note(self):
        data = {'id': '1', 'note': 'wow'}
        result = Order.edit_note(data, self.courier)
        ex_result = {'id': '1', 'note': 'wow'}
        self.assertEqual(result, ex_result)


class TestOrderContent(unittest.TestCase):
    def setUp(self):
        self.courier = s.query(User).filter(
            User.token == test_token().decode()).first()

    def test_6_order_content(self):
        data = {'id_order': 1}
        result = OrderContent.order_content(data, self.courier)
        ex_result = [
            {'id': '2', 'name': 'Лилии', 'subcategory_id': '1', 'photos': '', 'description': 'Нежно-белые лилии',
             'supplier_id': '1', 'price': '3242', 'show': '1', 'article': '324342'},
            {'id': '1', 'name': 'Красные розы', 'subcategory_id': '1', 'photos': '',
             'description': 'Длинные красные розы', 'supplier_id': '1', 'price': '4343', 'show': '1',
             'article': '324242'}]
        self.assertEqual(result, ex_result)


if __name__ == '__main__':
    unittest.main()
