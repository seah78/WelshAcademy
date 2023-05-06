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
        
        # add ingredient
        ingredient1 = {'name': 'Test Ingredient 1', 'description': 'Test description 1'}
        ingredient2 = {'name': 'Test Ingredient 2', 'description': 'Test description 2'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient1)
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient2)

        # get all ingredients
        response = self.client.get('/ingredient', headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Test Ingredient 1')
        self.assertEqual(data[0]['description'], 'Test description 1')
        self.assertEqual(data[1]['name'], 'Test Ingredient 2')
        self.assertEqual(data[1]['description'], 'Test description 2') 
    
    def test_show_one_ingredient(self):
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
        
        # add ingredient
        ingredient1 = {'name': 'Test Ingredient 1', 'description': 'Test description 1'}
        ingredient2 = {'name': 'Test Ingredient 2', 'description': 'Test description 2'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient1)
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient2)
        # get ingredient by id
        response = self.client.get(f'/ingredient/1', 
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)
        ingredient_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(ingredient_data['name'], ingredient1['name'])
        self.assertEqual(ingredient_data['description'], ingredient1['description'])
        
        # get ingredient by id that doesn't exist
        response = self.client.get(f'/ingredient/3', 
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 404)
        
    
    def test_update_ingredient(self):
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
        
        # add ingredient
        ingredient1 = {'name': 'Test Ingredient 1', 'description': 'Test description 1'}
        ingredient2 = {'name': 'Test Ingredient 2', 'description': 'Test description 2'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient1)
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient2)
        
                    
        # update ingredient
        updated_ingredient = {'name': 'Updated Ingredient Name', 
                              'description': 'Updated ingredient description'}
        response = self.client.put(f'/ingredient/2',
                                    headers={'x-access-token': token},
                                    json=updated_ingredient)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'Updated Ingredient Name')
        self.assertEqual(data['description'], 'Updated ingredient description')
