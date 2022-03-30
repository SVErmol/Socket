import unittest
from unittest.mock import patch, Mock
from client import *


# def test_data():
#     return {'phone':'123','password':'345'}
# def phone():
#     return 'phone':'123'
# def password():
#     return 345
class TestUser(unittest.TestCase):

    # data={'phone':'123','password':'345'}

    @patch('builtins.input', return_value='123')
    # @patch('builtins.input',return_value='345')
    def test_0_author(self, mock_input):
        query_client = {}
        # data = {}
        # data['phone'] = mock_input()
        # data['password'] = mock_input()
        result = author(query_client)
        ex_result = {'data': {'password': '123', 'phone': '123'}}
        self.assertEqual(result, ex_result)

    def test_1_edit_profile(self):
        data = {'name': 'Татьяна'}

        result = edit_profile(data)
        ex_result = {'name': 'Татьяна'}
        self.assertEqual(result, ex_result)

if __name__ == '__main__':
    unittest.main()
