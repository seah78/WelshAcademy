from flask import Flask

from config import Config
from api.user import user_api
from api.ingredient import ingredient_api
from api.recipe import recipe_api
from api.recipeingredient import recipe_ingredient_api
from api.favoriterecipe import favorite_recipe_api
from models.user import User
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from models.favorite_recipe import FavoriteRecipe


app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(ingredient_api)
app.register_blueprint(recipe_api)
app.register_blueprint(recipe_ingredient_api)
app.register_blueprint(favorite_recipe_api)

def init_app(app):
    from utils.extensions import db, ma
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        User.init_app(app)
        Ingredient.init_app(app)
        Recipe.init_app(app)
        RecipeIngredient.init_app(app)
        FavoriteRecipe.init_app(app)
        db.create_all()

app.config.from_object(Config)
init_app(app)

