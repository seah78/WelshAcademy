from utils.decorator import token_required
from flask import request, jsonify, Blueprint
from models.favorite_recipe import db, FavoriteRecipe, favorite_recipe_schema, favorites_recipes_schema

favorite_recipe_api = Blueprint('favorite_recipe_api', __name__)

# Favorite recipes endpoints

# New favorite recipe
@favorite_recipe_api.route('/favorite_recipe', methods=['POST'])
@token_required
def add_favorite_recipe(current_user):
    user_id = current_user.id
    recipe_id = request.json.get('recipe_id')
    new_favorite_recipe = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(new_favorite_recipe)
    db.session.commit()
    return favorite_recipe_schema.jsonify(new_favorite_recipe)

# Show all favorite recipe
@favorite_recipe_api.route('/favorite_recipe', methods=['GET'])
@token_required
def get_all_favorite_recipe(current_user):
    all_favorite_recipe = FavoriteRecipe.query.all()
    result = favorites_recipes_schema.dump(all_favorite_recipe)
    return jsonify(result)
    
# Show favorite recipe for current user
@favorite_recipe_api.route('/favorite_recipe', methods=['GET'])
@token_required
def get_favorite_recipe(current_user):
    user_id = current_user.id
    favorite_recipes = FavoriteRecipe.query.filter_by(user_id=user_id).all()
    result = favorites_recipes_schema.dump(favorite_recipes)
    return jsonify(result)


# Delete favorite recipe
@favorite_recipe_api.route('/favorite_recipe/<favorite_recipe_id>', methods=['DELETE'])
@token_required
def delete_favorite_recipe(current_user, favorite_recipe_id):
    favorite_recipe = FavoriteRecipe.query.get_or_404(favorite_recipe_id)
    if favorite_recipe.user_id is not current_user.id:
        return jsonify({'message' : 'Cannot perform that function!'})
    db.session.delete(favorite_recipe)
    db.session.commit()
    return jsonify({'message' : 'Favorite deleted!'}), 200


