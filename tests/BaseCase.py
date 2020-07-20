import datetime
import json
import unittest

from luizalab import app, db
from luizalab.database.models import Rule, User
from seed_rule import seed_rule
from seed_admin import seed_admin
from seed_products import seedProduct


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        db.create_all()
        seed_rule()
        seed_admin()
        seedProduct()

        payload = json.dumps({
            'email': 'admin@admin.com'
        })

        resp_user = self.app.post('/v1/signin', headers={'Content-type': 'application/json'}, data=payload)

        self.assertEqual(str, type(resp_user.json['access_token']))
        self.assertEqual(200, resp_user.status_code)

        self.access_token = resp_user.json['access_token']

    def tearDown(self):
        db.drop_all()
        db.session.close()