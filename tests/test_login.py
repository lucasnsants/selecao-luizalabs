import json

from test.BaseCase import BaseCase


class TestAuthLogin(BaseCase):
    def test_successfull_login(self):
        payload = json.dumps({
            'email': 'admin@admin.com'
        })

        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(str, type(response.json['access_token']))
        self.assertEqual(200, response.status_code)

    def test_login_already_exists(self):
        payload = json.dumps({
            'email': 'admin@admin.test'
        })

        response = self.app.post('/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual('Missing email parameter', response.json['msg'])
        self.assertEqual(400, response.status_code)