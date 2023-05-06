from utils.decorator import token_required
from flask import request, jsonify, Blueprint
from models.ingredient import db, Ingredient, ingredient_schema, ingredients_schema

ingredient_api = Blueprint('ingredient_api', __name__)

# Ingredient Endpoints

# New ingredient
@ingredient_api.route('/ingredient', methods=['POST'])
#@token_required
def add_ingredient(current_user):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    name = request.json['name']
    description = request.json.get('description', None)
    new_ingredient = Ingredient(name=name, description=description)
    db.session.add(new_ingredient)
    db.session.commit()
    return ingredient_schema.jsonify(new_ingredient)


# Show all indregients
@ingredient_api.route('/ingredient', methods=['GET'])
#@token_required
def get_all_ingredients(current_user):
    all_ingredients = Ingredient.query.all()
    
    
    result = ingredients_schema.dump(all_ingredients)
    return jsonify(result)

# Show ingredient by id
@ingredient_api.route('/ingredient/<ingredient_id>', methods=['GET'])
#@token_required
def get_ingredient(current_user, ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    return ingredient_schema.jsonify(ingredient)

# Update ingredient by id
@ingredient_api.route('/ingredient/<ingredient_id>', methods=['PUT'])
#@token_required
def update_ingredient(current_user, ingredient_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    ingredient.name = request.json['name']
    ingredient.description = request.json.get('description', None)
    db.session.commit()
    return ingredient_schema.jsonify(ingredient)