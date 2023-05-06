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

from utils.extensions import db

class TestRecipeIngredient(BaseTestCase):

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

        # add ingredient
        ingredient = {'name': 'Test Ingredient', 'description': 'Test description'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient)
        self.assertEqual(response.status_code, 200)

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

        # add ingredient to recipe
        recipe_ingredient = {
            'recipe_id': recipe_id,
            'ingredient_id': 1,
            'quantity': 2
        }
        response = self.client.post('/recipe_ingredient',
                                    headers={'x-access-token': token},
                                    json=recipe_ingredient)
        self.assertEqual(response.status_code, 200)



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

        # add ingredient
        ingredient = {'name': 'Test Ingredient', 'description': 'Test description'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient)
        self.assertEqual(response.status_code, 200)

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

        # add ingredient to recipe
        recipe_ingredient = {
            'recipe_id': recipe_id,
            'ingredient_id': 1,
            'quantity': 2
        }
        response = self.client.post('/recipe_ingredient', 
                                    headers={'x-access-token': token},
                                    json=recipe_ingredient)
        self.assertEqual(response.status_code, 200)

        # show all recipe ingredients
        response = self.client.get('/recipe_ingredient', headers={'x-access-token': token})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)
 
                    
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

        # add ingredient
        ingredient = {'name': 'Test Ingredient', 'description': 'Test description'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient)
        self.assertEqual(response.status_code, 200)

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

        # add ingredient to recipe
        recipe_ingredient = {
            'recipe_id': recipe_id,
            'ingredient_id': 1,
            'quantity': 2
        }
        response = self.client.post('/recipe_ingredient', 
                                    headers={'x-access-token': token},
                                    json=recipe_ingredient)
        self.assertEqual(response.status_code, 200)
        
                
    def test_update_recipe_ingredient(self):
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
        ingredient = {'name': 'Test Ingredient', 'description': 'Test description'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient)
        self.assertEqual(response.status_code, 200)

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

        # add ingredient to recipe
        recipe_ingredient = {
            'recipe_id': recipe_id,
            'ingredient_id': 1,
            'quantity': 2
        }
        response = self.client.post('/recipe_ingredient', 
                                    headers={'x-access-token': token},
                                    json=recipe_ingredient)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        recipe_ingredient_id = data['id']

        # update ingredient in recipe
        recipe_ingredient_update = {
            'recipe_id': recipe_id,
            'ingredient_id': 1,
            'quantity': 3
        }
        response = self.client.put('/recipe_ingredient/{}'.format(recipe_ingredient_id), 
                                    headers={'x-access-token': token},
                                    json=recipe_ingredient_update)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['quantity'], '3')
        
    def test_delete_recipe_ingredient(self):
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
        ingredient = {'name': 'Test Ingredient', 'description': 'Test description'}
        response = self.client.post('/ingredient', 
                                    headers={'x-access-token': token},
                                    json=ingredient)
        self.assertEqual(response.status_code, 200)

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

        # add ingredient to recipe
        recipe_ingredient = {
            'recipe_id': recipe_id,
            'ingredient_id': 1,
            'quantity': 2
        }

        response = self.client.post('/recipe_ingredient', 
                                    headers={'x-access-token': token},
                                    json=recipe_ingredient)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue('id' in data)
        recipe_ingredient_id = data['id']

        # delete recipe ingredient
        response = self.client.delete(f'/recipe_ingredient/{recipe_ingredient_id}', 
                                        headers={'x-access-token': token})
        self.assertEqual(response.status_code, 204)


