import pytest
from unittest import mock
from flask import Flask

from app import *


@pytest.fixture(scope='session')
def app():
    app = Flask('name')
    app.register_blueprint(user_api)
    app.register_blueprint(ingredient_api)
    app.register_blueprint(recipe_api)
    app.register_blueprint(recipe_ingredient_api)
    app.register_blueprint(favorite_recipe_api)

    app.config.from_object('config.TestConfig')
    
    with app.app_context():
        from utils.extensions import db, ma
        db.init_app(app)
        ma.init_app(app)
        
        User.init_app(app)
        Ingredient.init_app(app)
        Recipe.init_app(app)
        RecipeIngredient.init_app(app)
        FavoriteRecipe.init_app(app)
        
        db.create_all()

    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        from utils.extensions import db
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def mock_user():
    user = mock.Mock()
    user.id = 1
    user.username = 'mockuser'
    user.password = '123456'
    return user


@pytest.fixture(scope='function')
def mock_admin():
    user = mock.Mock()
    user.id = 1
    user.username = 'SuperAdmin'
    user.password = 'SuperPassword'
    return user


@pytest.fixture(scope='function')
def mock_recipe():
    recipe = mock.Mock()
    recipe.id = 1
    recipe.title = 'Mock Recipe'
    recipe.description = 'This is a mock recipe.'
    recipe.user_id = 1
    return recipe


@pytest.fixture(scope='function')
def mock_ingredient():
    ingredient = mock.Mock()
    ingredient.id = 1
    ingredient.name = 'Mock Ingredient'
    ingredient.description = 'This is a mock ingredient.'
    return ingredient


@pytest.fixture(scope='function')
def mock_recipe_ingredient():
    recipe_ingredient = mock.Mock()
    recipe_ingredient.id = 1
    recipe_ingredient.recipe_id = 1
    recipe_ingredient.ingredient_id = 1
    recipe_ingredient.quantity = 1
    recipe_ingredient.unit = 'unit'
    return recipe_ingredient


@pytest.fixture(scope='function')
def mock_favorite_recipe():
    favorite_recipe = mock.Mock()
    favorite_recipe.id = 1
    favorite_recipe.user_id = 1
    favorite_recipe.recipe_id = 1
    return favorite_recipe
