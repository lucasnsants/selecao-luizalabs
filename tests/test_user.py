import datetime
import json

from tests.BaseCase import BaseCase


class TestUser(BaseCase):
    def test_successful_list_user(self):
        resp_users = self.app.get('/v1/users/', headers={'Authorization': 'Bearer {}'.format(self.access_token)})

        self.assertEqual(1, resp_users.json['total_count'])
        self.assertEqual(200, resp_users.status_code)

    def test_successful_new_user(self):
        payload = json.dumps({
            'name': 'Test New User',
            'email': 'test@test.com',
            'rule_id': 2
        })

        resp_user = self.app.post('/v1/users/',
            headers={'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self.access_token)},
            data=payload)

        self.assertEqual('Test New User', resp_user.json['name'])
        self.assertEqual(201, resp_user.status_code)

    def test_without_permission_user(self):
        register = json.dumps({
            'name': 'Lucas Nascimento Santos',
            'email': 'lucas@test.com',
            'rule_id': 2
        })

        resp_login = self.app.post('/v1/signup',
            headers={'Content-type': 'application/json'},
            data=register)

        self.assertEqual(201, resp_login.status_code)

        resp_users = self.app.get('/v1/users/',
            headers={'Authorization': 'Bearer {}'.format(resp_login.json['access_token'])})

        self.assertEqual('Admins only!', resp_users.json['msg'])
        self.assertEqual(403, resp_users.status_code)

    # def test_get_info_user_current_user(self):
    #     register = json.dumps({
    #         'name': 'Lucas Nascimento Santos',
    #         'email': 'lucas@test.com',
    #         'rule_id': 2
    #     })

    #     resp_login = self.app.post('/v1/signup',
    #         headers={'Content-type': 'application/json'},
    #         data=register)

    #     self.assertEqual(201, resp_login.status_code)

    #     resp_users = self.app.get('/v1/user/',
    #         headers={'Authorization': 'Bearer {}'.format(resp_login.json['access_token'])})

    #     self.assertEqual('Lucas Nascimento Santos', resp_users.json['name'])
    #     self.assertEqual(200, resp_users.status_code)