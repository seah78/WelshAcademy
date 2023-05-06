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
from models.recipe_ingredient import RecipeIngredient
from models.recipe import Recipe
from models.favorite_recipe import FavoriteRecipe

from utils.extensions import db

class TestFavoriteRecipe(BaseTestCase):

    def test_add_favorite_recipe(self):
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

        # Add recipe
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

        # Add favorite recipe
        response = self.client.post('/favorite_recipe',
                                    headers={'x-access-token': token},
                                    json={'recipe_id': recipe_id})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        self.assertEqual(data['user_id'], superadmin.id)
        self.assertEqual(data['recipe_id'], recipe_id)

    def test_get_all_favorite_recipe(self):
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

        # Add recipe
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

        # Add favorite recipe
        response = self.client.post('/favorite_recipe',
                                    headers={'x-access-token': token},
                                    json={'recipe_id': recipe_id})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        
        # Get all favorite recipes
        response = self.client.get('/favorite_recipe',
                                headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

                
    def test_favorite_recipe(self):
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

        # Add recipe
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

        # Add favorite recipe
        response = self.client.post('/favorite_recipe',
                                    headers={'x-access-token': token},
                                    json={'recipe_id': recipe_id})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        
        # Get favorite recipe for current user (1 item)
        response = self.client.get('/favorite_recipe',
                                    headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)    

    def test_delete_favorite_recipe(self):
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

        # Add recipe
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

        # Add favorite recipe
        response = self.client.post('/favorite_recipe',
                                    headers={'x-access-token': token},
                                    json={'recipe_id': recipe_id})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        favorite_recipe_id = data['id']

        # Delete favorite recipe
        response = self.client.delete(f'/favorite_recipe/{favorite_recipe_id}',
                                        headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Favorite deleted!')
