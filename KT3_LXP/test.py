import requests
from pprint import pprint
from unittest import TestCase
import unittest


class Api:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, body):
        response = requests.post(f'{self.base_url}/{endpoint}', json=body)
        try:
            return (response.status_code, response.json())
        except ValueError:
            return (response.status_code, response.text)

    def get(self, endpoint):
        response = requests.get(f'{self.base_url}/{endpoint}')
        try:
            return (response.status_code, response.json())
        except ValueError:
            return (response.status_code, response.text)

    def put(self, endpoint, body):
        response = requests.put(f'{self.base_url}/{endpoint}', json=body)
        try:
            return (response.status_code, response.json())
        except ValueError:
            return (response.status_code, response.text)

    def delete(self, endpoint):
        response = requests.delete(f'{self.base_url}/{endpoint}')
        try:
            return (response.status_code, response.json())
        except ValueError:
            return (response.status_code, response.text)


class Tests(TestCase):
    api = Api('https://petstore.swagger.io/v2')

    def test_create_user(self):
        user = {
            'id': 1001,
            'username': 'test_user',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@example.com',
            'password': 'password',
            'phone': '1234567890',
            'userStatus': 1,
        }
        status, body = self.api.post('user', user)
        self.assertEqual(status, 200)

    def test_get_user_by_name(self):
        username = 'test_user'
        status, body = self.api.get(f'user/{username}')
        self.assertEqual(status, 200)
        self.assertEqual(body.get('username'), username)

    def test_login_user(self):
        status, body = self.api.get('user/login?username=test_user_qa&password=password')
        self.assertEqual(status, 200)
        self.assertIsInstance(body, dict)

    def test_logout_user(self):
        status, body = self.api.get('user/logout')
        self.assertEqual(status, 200)

    def test_get_inventory(self):
        status, body = self.api.get('store/inventory')
        self.assertEqual(status, 200)
        self.assertIsInstance(body, dict)

    def test_place_order(self):
        order = {
            'id': 1,
            'petId': 1,
            'quantity': 2,
            'shipDate': '2024-01-01T00:00:00.000Z',
            'status': 'placed',
            'complete': False,
        }
        status, body = self.api.post('store/order', order)
        self.assertEqual(status, 200)
        self.assertEqual(body.get('id'), order['id'])
        self.assertEqual(body.get('status'), 'placed')

    def test_get_order_by_id(self):
        order_id = 1
        status, body = self.api.get(f'store/order/{order_id}')
        self.assertEqual(status, 200)
        self.assertEqual(body.get('id'), order_id)

    def test_delete_order(self):
        order_id = 1
        status, body = self.api.delete(f'store/order/{order_id}')
        self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()