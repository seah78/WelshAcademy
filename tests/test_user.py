import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json

from tests.base_tests import BaseTestCase
from models.user import User
from utils.extensions import db

class TestUser(BaseTestCase):

    def test_create_admin_user(self):
        # send a POST request to the /admin route
        response = self.client.post('/admin')

        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # assert that the response message is "SuperAdmin created"
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'SuperAdmin created')

        # assert that the SuperAdmin user was created in the database
        superadmin = User.query.filter_by(username='SuperAdmin').first()
        self.assertIsNotNone(superadmin)
