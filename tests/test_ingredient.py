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
from models.ingredient import Ingredient
from utils.extensions import db

class TestIngredient(BaseTestCase):
    
    def test_add_ingredient(self):
        superadmin = User(public_id='superadmin', 
                        username='SuperAdmin', 
                        password=generate_password_hash('SuperPassword'), 
                        is_admin=True)
        db.session.add(superadmin)
        db.session.commit()

        # Login as superadmin and get token
        response = self.client.get('/login', headers={
            'Authorization': 'Basic ' + b64encode(b'SuperAdmin:SuperPassword').decode('utf-8')
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('token' in data)
        token = data['token']
        
        # Test adding a new ingredient
        ingredient = {'name': 'Test Ingredient', 'description': 'Test description'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], ingredient['name'])
        self.assertEqual(data['description'], ingredient['description']) 
        
        
        
        
    def test_show_all_ingredients(self):
        pass
    
    def test_show_one_ingredient(self):
        pass
    
    def test_updae_ingredient(self):
        pass    
    
