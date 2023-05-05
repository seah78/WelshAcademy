from utils.decorator import token_required
from flask import request, jsonify, Blueprint
from models.recipe import db, Recipe, recipe_schema, recipes_schema
from models.recipe_ingredient import RecipeIngredient, recipe_ingredient_schema

recipe_api = Blueprint('recipe_api', __name__)

# Recipe endpoints

# New recipe
@recipe_api.route('/recipe', methods=['POST'])
#@token_required
def add_recipe(current_user):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    name = request.json['name']
    description = request.json.get('description', None)
    new_recipe = Recipe(name=name, description=description)
    db.session.add(new_recipe)
    
    for ingredient in request.json.get('ingredients', []):
        ingredient_id = ingredient['id']
        quantity = ingredient['quantity']
        recipe_ingredient = RecipeIngredient(recipe=new_recipe, ingredient_id=ingredient_id, quantity=quantity)
        db.session.add(recipe_ingredient)

    db.session.commit()
    return recipe_schema.jsonify(new_recipe)

# Show all recipes
@recipe_api.route('/recipe', methods=['GET'])
#@token_required
def get_all_recipes(current_user):
    all_recipes = Recipe.query.all()
    result = []
    for recipe in all_recipes:
        recipe_data = recipe_schema.dump(recipe)
        recipe_data['ingredients'] = [recipe_ingredient_schema.dump(ingredient) for ingredient in recipe.ingredients]
        result.append(recipe_data)
    return jsonify(result), 200

# Show recipe by id with its ingredients
@recipe_api.route('/recipe/<recipe_id>', methods=['GET'])
#@token_required
def get_recipe(current_user, recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe_data = recipe_schema.dump(recipe)
    recipe_data['ingredients'] = [recipe_ingredient_schema.dump(ingredient) for ingredient in recipe.ingredients]
    return jsonify(recipe_data), 200

# Update recipe by id
@recipe_api.route('/recipe/<recipe_id>', methods=['PUT'])
#@token_required
def update_recipe(current_user, recipe_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.name = request.json['name']
    recipe.description = request.json.get('description', None)
    recipe.ingredients = []
    for ingredient in request.json.get('ingredients', []):
        ingredient_id = ingredient['id']
        quantity = ingredient['quantity']
        recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient_id=ingredient_id, quantity=quantity)
        db.session.add(recipe_ingredient)

    db.session.commit()
    return recipe_schema.jsonify(recipe)