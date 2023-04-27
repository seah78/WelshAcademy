from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

class IngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'ingredients')

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


# RecipeIngredient Model
class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.String(20), nullable=False)

    def __init__(self, recipe_id, ingredient_id, quantity):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity

class RecipeIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'recipe_id', 'ingredient_id', 'quantity')

recipe_ingredient_schema = RecipeIngredientSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)


# FavoriteRecipe Model
class FavoriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id
        
class FavoriteRecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'recipe_id')

favorite_recipe_schema = FavoriteRecipeSchema()
favorites_recipes_schema = FavoriteRecipeSchema(many=True)


def init_app(app):
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()


