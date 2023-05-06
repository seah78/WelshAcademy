from utils.decorator import token_required
from flask import request, jsonify, Blueprint
from models.recipe_ingredient import (
    db,
    RecipeIngredient,
    recipe_ingredient_schema,
    recipe_ingredients_schema,
)
from models.recipe import recipe_schema

recipe_ingredient_api = Blueprint("recipe_ingredient_api", __name__)

# Ingredients Recipe endpoints


# New ingredient in recipe
@recipe_ingredient_api.route("/recipe_ingredient", methods=["POST"])
@token_required
def add_recipe_ingredient(current_user):
    if not current_user.is_admin:
        return jsonify({"message": "Cannot perform that function!"})

    recipe_id = request.json["recipe_id"]
    ingredient_id = request.json["ingredient_id"]
    quantity = request.json["quantity"]
    new_recipe_ingredient = RecipeIngredient(
        recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity
    )

    db.session.add(new_recipe_ingredient)
    db.session.commit()
    return recipe_schema.jsonify(new_recipe_ingredient)


# Show all ingredient in recipe
@recipe_ingredient_api.route("/recipe_ingredient", methods=["GET"])
@token_required
def get_all_recipes_ingredient(current_user):
    all_recipe_ingredients = RecipeIngredient.query.all()
    result = recipe_ingredients_schema.dump(all_recipe_ingredients)
    return jsonify(result)


# Show ingredient in recipe by id
@recipe_ingredient_api.route(
    "/recipe_ingredient/<recipe_ingredient_id>", methods=["GET"]
)
@token_required
def get_recipe_ingredient(current_user, recipe_ingredient_id):
    recipe_ingredient = RecipeIngredient.query.get_or_404(recipe_ingredient_id)
    return recipe_ingredient_schema.jsonify(recipe_ingredient)


# Update ingredient in recipe by id
@recipe_ingredient_api.route(
    "/recipe_ingredient/<recipe_ingredient_id>", methods=["PUT"]
)
@token_required
def update_recipe_ingredient(current_user, recipe_ingredient_id):
    if not current_user.is_admin:
        return jsonify({"message": "Cannot perform that function!"})
    recipe_ingredient = RecipeIngredient.query.get_or_404(recipe_ingredient_id)
    recipe_ingredient.recipe_id = request.json["recipe_id"]
    recipe_ingredient.ingredient_id = request.json["ingredient_id"]
    recipe_ingredient.quantity = request.json["quantity"]
    db.session.commit()
    return recipe_ingredient_schema.jsonify(recipe_ingredient)


# Delete ingredien in recipe by id
@recipe_ingredient_api.route(
    "/recipe_ingredient/<recipe_ingredient_id>", methods=["DELETE"]
)
@token_required
def delete_recipe_ingredient(current_user, recipe_ingredient_id):
    if not current_user.is_admin:
        return jsonify({"message": "Cannot perform that function!"})
    recipe_ingredient = RecipeIngredient.query.get_or_404(recipe_ingredient_id)
    db.session.delete(recipe_ingredient)
    db.session.commit()
    return "", 204
