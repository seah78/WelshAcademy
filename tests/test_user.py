from base64 import b64encode
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

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

    def test_login_success(self):
        # create a test user
        password = 'test_password'
        user = User(public_id="test", username='test_user', password=generate_password_hash(password), is_admin=False)
        db.session.add(user)
        db.session.commit()

        # send a POST request to the /login route with basic authentication header
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'test_user:test_password').decode('utf-8')
        })

        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # assert that the response contains a valid JWT token
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        decoded_token = jwt.decode(data['token'], current_app.config['SECRET_KEY'])
        self.assertEqual(decoded_token['public_id'], str(user.public_id))

    def test_login_failure(self):
        # send a POST request to the /login route with incorrect credentials
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'wrong_user:wrong_password').decode('utf-8')
        })

        # assert that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, 401)

        # assert that the response contains a valid WWW-Authenticate header
        self.assertTrue('WWW-Authenticate' in response.headers)
