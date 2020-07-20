import datetime
import json

from tests.BaseCase import BaseCase


class TestFavorite(BaseCase):
    def test_successful_new_favorite(self):
        payload = json.dumps({
            "product_id": 1
        })

        resp_fav = self.app.post('/v1/favorite/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('Cake - Night And Day Choclate', resp_fav.json['title'])
        self.assertEqual(201, resp_fav.status_code)

    def test_not_fount_product(self):
        payload = json.dumps({
            "product_id": 99
        })

        resp_fav = self.app.post('/v1/favorite/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('Product not found.', resp_fav.json['msg'])
        self.assertEqual(404, resp_fav.status_code)

    def test_product_duplicate(self):
        payload = json.dumps({
            "product_id": 1
        })

        resp_fav1 = self.app.post('/v1/favorite/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('Cake - Night And Day Choclate', resp_fav1.json['title'])
        self.assertEqual(201, resp_fav1.status_code)

        resp_fav2 = self.app.post('/v1/favorite/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('Product duplicate.', resp_fav2.json['msg'])
        self.assertEqual(409, resp_fav2.status_code)

    def test_delete_favorite(self):
        payload = json.dumps({
            "product_id": 1
        })

        resp_fav = self.app.post('/v1/favorite/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('Cake - Night And Day Choclate', resp_fav.json['title'])
        self.assertEqual(201, resp_fav.status_code)

        resp_del = self.app.delete('/v1/favorite/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('successful deletion.', resp_del.json['msg'])
        self.assertEqual(201, resp_del.status_code)
        