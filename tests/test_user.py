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
    
    def test_get_all_users(self):

        # Test with an admin user
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(len(json.loads(response.data)['users']), 2)
        
        # Test with a non-admin user
        #response = self.client.get('/user')
        #self.assertEqual(response.status_code, 401)
        
    def test_get_one_user(self):
        # Test with a non-admin user
        response = self.client.get('/user/' + self.test_user.public_id)
        self.assertEqual(response.status_code, 401)

        # Test with an admin user
        response = self.client.get('/user/' + self.test_user.public_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['user']['public_id'], self.test_user.public_id)

    def test_signup(self):

        # Test with a new username
        response = self.client.post('/signup', json={'username': 'newuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'New user created')

        # Test with an existing username
        response = self.client.post('/signup', json={'username': 'newuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 409)

