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
from models.recipe import Recipe
from utils.extensions import db

class TestRecipe(BaseTestCase):

    def test_add_recipe(self):
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

        # add recipe
        recipe = {
            'name': 'Test Recipe',
            'description': 'Test Recipe Description',
            'ingredients': []
        }
        response = self.client.post('/recipe',
                                    headers={'x-access-token': token},
                                    json=recipe)
        self.assertEqual(response.status_code, 200)
        

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        recipe_id = data['id']
        
        # check if recipe exists in database
        recipe = Recipe.query.get(recipe_id)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, 'Test Recipe')
        self.assertEqual(recipe.description, 'Test Recipe Description')

    def test_show_all_recipes(self):
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

        # add recipe
        recipe = {
            'name': 'Test Recipe',
            'description': 'Test Recipe Description',
            'ingredients': []
        }
        response = self.client.post('/recipe',
                                    headers={'x-access-token': token},
                                    json=recipe)
        self.assertEqual(response.status_code, 200)
        

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        
        # show all recipes
        response = self.client.get('/recipe', headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertTrue('id' in data[0])
        self.assertTrue('name' in data[0])
        self.assertTrue('description' in data[0])
        self.assertTrue('ingredients' in data[0])
        self.assertIsInstance(data[0]['ingredients'], list)
        self.assertEqual(len(data[0]['ingredients']), 0)

        
    def test_show_one_recipe(self):
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

        # add recipe
        recipe = {
            'name': 'Test Recipe',
            'description': 'Test Recipe Description',
            'ingredients': []
        }
        response = self.client.post('/recipe',
                                    headers={'x-access-token': token},
                                    json=recipe)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        recipe_id = data['id']
        
        # get recipe by id
        response = self.client.get(f'/recipe/{recipe_id}', headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], recipe_id)
        self.assertEqual(data['name'], 'Test Recipe')
        self.assertEqual(data['description'], 'Test Recipe Description')
        self.assertEqual(len(data['ingredients']), 0)

        
            
    def test_update_recipe(self):
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

        # add recipe
        recipe = {
            'name': 'Test Recipe',
            'description': 'Test Recipe Description',
            'ingredients': []
        }
        response = self.client.post('/recipe',
                                    headers={'x-access-token': token},
                                    json=recipe)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        recipe_id = data['id']

        # update recipe
        updated_recipe = {
            'name': 'Updated Test Recipe',
            'description': 'Updated Test Recipe Description',
            'ingredients': []
        }
        response = self.client.put(f'/recipe/{recipe_id}',
                                    headers={'x-access-token': token},
                                    json=updated_recipe)
        self.assertEqual(response.status_code, 200)
        
        # check if recipe was updated
        response = self.client.get(f'/recipe/{recipe_id}', headers={'x-access-token': token})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'Updated Test Recipe')
        self.assertEqual(data['description'], 'Updated Test Recipe Description')

