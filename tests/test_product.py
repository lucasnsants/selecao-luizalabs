import datetime
import json

from test.BaseCase import BaseCase
from models import User

class TestProduct(BaseCase):
    def test_succeesful_list_product(self):
        resp_products = self.app.get('/product/', 
            headers={'Authorization': 'Bearer {}'.format(self.access_token)}, 
            query_string=dict(page=1, limit=10))

        self.assertEqual(10, resp_products.json['page_size'])
        self.assertEqual(200, resp_products.status_code)

    def test_product_without_token(self):
        resp_products = self.app.get('/product/', query_string=dict(page=2, limit=5))

        self.assertEqual('Missing Authorization Header', resp_products.json['msg'])
        self.assertEqual(401, resp_products.status_code)

    def test_product_limit_per_page(self):
        resp_products = self.app.get('/product/', headers={'Authorization': 'Bearer {}'.format(self.access_token)}, query_string=dict(page=1, limit=5))

        self.assertEqual(5, resp_products.json['page_size'])
        self.assertEqual(200, resp_products.status_code)

    def test_new_product(self):
        new_product = json.dumps({
            "title": "iPhone XR",
            "brand": "Apple",
            "image": "http://dummyimage.com/103x153.bmp/ff4444/ffffff",
            "price": 100.3,
            "review_score": "3.39"
        })

        resp_product = self.app.post('/product/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=new_product)

        self.assertEqual(dict, type(resp_product.json))
        self.assertEqual('iPhone XR', resp_product.json['title'])
        self.assertEqual(201, resp_product.status_code)

    def test_get_product_per_id(self):
        resp_product = self.app.get('/product/1',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)})
        
        self.assertEqual(dict, type(resp_product.json))
        self.assertEqual('Cake - Night And Day Choclate', resp_product.json['title'])
        self.assertEqual(200, resp_product.status_code)

    def test_product_already_exists_per_id(self):
        resp_product = self.app.get('/product/99',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)})
        
        self.assertEqual(dict, type(resp_product.json))
        self.assertEqual("99 doesn't exist", resp_product.json['msg'])
        self.assertEqual(404, resp_product.status_code)

    def test_put_product_per_id(self):
        payload = json.dumps({
            'title': 'Cake - Night And Day Choclate Test',
            'brand': 'Apple',
            'image': 'http://dummyimage.com/103x153.bmp/ff4444/ffffff',
            'price': 99.3,
            'review_score': '3.39'
        })

        resp_product = self.app.put('/product/1',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual(dict, type(resp_product.json))
        self.assertEqual('Cake - Night And Day Choclate Test', resp_product.json['title'])
        self.assertEqual(200, resp_product.status_code)

    def test_delete_product_per_id(self):
        resp_product = self.app.delete('/product/1',
            headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        
        self.assertEqual('successful deletion.', resp_product.json['msg'])
        self.assertEqual(201, resp_product.status_code)