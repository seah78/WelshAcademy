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
        
    def test_update_admin_user(self):
        # create a super user
        superadmin = User(public_id='superadmin', 
                          username='SuperAdmin', 
                          password=generate_password_hash('SuperPassword'), 
                          is_admin=True)
        db.session.add(superadmin)
        db.session.commit()
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'SuperAdmin:SuperPassword').decode('utf-8')
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        token = data['token']
        # update the SuperAdmin user password
        new_password = 'NewSuperPassword'
        response = self.client.put('/admin', json={'new_password': new_password}, headers={
            'x-access-token': token
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'SuperAdmin password updated')

        # log in with the new password and check if it works
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'SuperAdmin:' + new_password.encode()).decode('utf-8')
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        
    def test_show_all_users(self):
        superadmin = User(public_id='superadmin', 
                        username='SuperAdmin', 
                        password=generate_password_hash('SuperPassword'), 
                        is_admin=True)
        user = User(public_id="test", 
                    username='test_user', 
                    password=generate_password_hash('test_password'), 
                    is_admin=False)
        db.session.add(superadmin)
        db.session.add(user)
        db.session.commit()

        # Login as superadmin and get token
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'SuperAdmin:SuperPassword').decode('utf-8')
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        token = data['token']

        # Get all users with the token
        response = self.client.get('/user', headers={
            'x-access-token': token
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))

        # Check if the returned data matches the expected data
        self.assertEqual(len(data['users']), 2)
        self.assertEqual(data['users'][0]['public_id'], superadmin.public_id)
        self.assertEqual(data['users'][0]['username'], superadmin.username)
        self.assertEqual(data['users'][0]['is_admin'], superadmin.is_admin)
        self.assertEqual(data['users'][1]['public_id'], user.public_id)
        self.assertEqual(data['users'][1]['username'], user.username)
        self.assertEqual(data['users'][1]['is_admin'], user.is_admin)

    def test_show_one_user(self):
        superadmin = User(public_id='superadmin', 
                        username='SuperAdmin', 
                        password=generate_password_hash('SuperPassword'), 
                        is_admin=True)
        user = User(public_id="test", 
                    username='test_user', 
                    password=generate_password_hash('test_password'), 
                    is_admin=False)
        db.session.add(superadmin)
        db.session.add(user)
        db.session.commit()

        # Login as superadmin and get token
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'SuperAdmin:SuperPassword').decode('utf-8')
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        token = data['token']
        
        # Get the user using its public_id
        response = self.client.get(f'/user/{user.public_id}', headers={
            'x-access-token': token
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['user']['public_id'], user.public_id)
        self.assertEqual(data['user']['username'], user.username)
        self.assertEqual(data['user']['password'], user.password)
        self.assertEqual(data['user']['is_admin'], user.is_admin)

    def test_delete_one_user(self):
        superadmin = User(public_id='superadmin', 
                        username='SuperAdmin', 
                        password=generate_password_hash('SuperPassword'), 
                        is_admin=True)
        user = User(public_id="test", 
                    username='test_user', 
                    password=generate_password_hash('test_password'), 
                    is_admin=False)
        db.session.add(superadmin)
        db.session.add(user)
        db.session.commit()

        # Login as superadmin and get token
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'SuperAdmin:SuperPassword').decode('utf-8')
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        token = data['token']
            
        # Delete the user using its public_id
        response = self.client.delete(f'/user/{user.public_id}', headers={
            'x-access-token': token
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'The user has been deleted!')
        


    def test_login_success(self):
        # create a test user
        user = User(public_id="test", 
                    username='test_user', 
                    password=generate_password_hash('test_password'), 
                    is_admin=False)
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


