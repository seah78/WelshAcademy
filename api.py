import datetime
from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

from config import Config
from models import db, User, Ingredient, Recipe, RecipeIngredient, FavoriteRecipe, init_app, ingredient_schema, ingredients_schema, recipe_ingredient_schema, recipe_ingredients_schema, recipe_schema, recipes_schema, favorite_recipe_schema, favorites_recipes_schema

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

# decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



# ENDPONTS

# home
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welsh Academy</h1><p>Welsh Academy's API site.</p>"

# User endpoints

# Create admin user
@app.route('/admin', methods=['POST'])
def create_admin_user():
    
    hashed_password = generate_password_hash("SuperPassword", method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), username="SuperAdmin", password=hashed_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'SuperAdmin created'})

# Updtae password user

# Show all users
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['is_admin'] = user.is_admin
        output.append(user_data)

    return jsonify({'users' : output})

# Show one user
@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify({'message' : 'User not found'})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['is_admin'] = user.is_admin
    
    return jsonify({'user' : user_data})

# Create user
@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'New user created'})

# Update user
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def update_user(current_user, public_id):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify({'message' : 'User not found'})

    user.is_admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been updated!'})

# Delete user
@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

# Login
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

# Ingredient Endpoints

# New ingredient
@app.route('/ingredient', methods=['POST'])
@token_required
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
@app.route('/ingredient', methods=['GET'])
@token_required
def get_all_ingredients(current_user):
    all_ingredients = Ingredient.query.all()
    
    
    result = ingredients_schema.dump(all_ingredients)
    return jsonify(result)

# Show ingredient by id
@app.route('/ingredient/<ingredient_id>', methods=['GET'])
@token_required
def get_ingredient(current_user, ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    return ingredient_schema.jsonify(ingredient)

# Update ingredient by id
@app.route('/ingredient/<ingredient_id>', methods=['PUT'])
@token_required
def update_ingredient(current_user, ingredient_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    ingredient.name = request.json['name']
    ingredient.description = request.json.get('description', None)
    db.session.commit()
    return ingredient_schema.jsonify(ingredient)

# Delete ingredient by id
@app.route('/ingredient/<ingredient_id>', methods=['DELETE'])
@token_required
def delete_ingredient(current_user, ingredient_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    return '', 204



# Recipe endpoints

# New recipe
@app.route('/recipe', methods=['POST'])
@token_required
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
@app.route('/recipe', methods=['GET'])
@token_required
def get_all_recipes(current_user):
    all_recipes = Recipe.query.all()
    result = recipes_schema.dump(all_recipes)
    return jsonify(result)

# Show recipe by id
@app.route('/recipe/<recipe_id>', methods=['GET'])
@token_required
def get_recipe(current_user, recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return recipe_schema.jsonify(recipe)

# Update recipe by id
@app.route('/recipe/<recipe_id>', methods=['PUT'])
@token_required
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

# Delete recipe by id
@app.route('/recipe/<recipe_id>', methods=['DELETE'])
@token_required
def delete_recipe(current_user, recipe_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return '', 204


# Ingredients Recipe endpoints

# New ingredient in recipe
@app.route('/recipe_ingredient', methods=['POST'])
@token_required
def add_recipe_ingredient(current_user):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    recipe_id = request.json['recipe_id']
    ingredient_id = request.json['ingredient_id']
    quantity = request.json['quantity']
    new_recipe_ingredient = RecipeIngredient(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity)
    
    db.session.add(new_recipe_ingredient)
    db.session.commit()
    return recipe_schema.jsonify(new_recipe_ingredient)

# Show all ingredient in recipe
@app.route('/recipe', methods=['GET'])
@token_required
def get_all_recipes_ingredient(current_user):
    all_recipe_ingredients = RecipeIngredient.query.all()
    result = recipe_ingredients_schema.dump(all_recipe_ingredients)
    return jsonify(result)

# Show ingredient in recipe by id
@app.route('/recipe/<recipe_ingredient_id>', methods=['GET'])
@token_required
def get_recipe_ingredient(current_user, recipe_ingredient_id):
    recipe_ingredient = RecipeIngredient.query.get_or_404(recipe_ingredient_id)
    return recipe_ingredient_schema.jsonify(recipe_ingredient)

# Update ingredient in recipe by id
@app.route('/recipe/<recipe_ingredient_id>', methods=['PUT'])
@token_required
def update_recipe_ingredient(current_user, recipe_ingredient_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    recipe_ingredient = RecipeIngredient.query.get_or_404(recipe_ingredient_id)
    recipe_ingredient.recipe_id = request.json['recipe_id']
    recipe_ingredient.ingredient_id = request.json['ingredient_id']
    recipe_ingredient.quantity = request.json['quantity']
    db.session.commit()
    return recipe_ingredient_schema.jsonify(recipe_ingredient)

# Delete recipe by id
@app.route('/recipe/<recipe_ingredient_id>', methods=['DELETE'])
@token_required
def delete_recipe_ingredient(current_user, recipe_ingredient_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    recipe_ingredient = RecipeIngredient.query.get_or_404(recipe_ingredient_id)
    db.session.delete(recipe_ingredient)
    db.session.commit()
    return '', 204


# Favorite recipes endpoints

# New favorite recipe
@app.route('/favorite_recipe', methods=['POST'])
@token_required
def add_favorite_recipe(current_user):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user_id = request.json['user_id']
    recipe_id = request.json.get('recipe_id')
    new_favorite_recipe = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
    db.session.add(new_favorite_recipe)
    db.session.commit()
    return favorite_recipe_schema.jsonify(new_favorite_recipe)

# Show all favorite recipe
@app.route('/favorite_recipe', methods=['GET'])
@token_required
def get_all_favorite_recipe(current_user):
    all_favorite_recipe = FavoriteRecipe.query.all()
    result = favorites_recipes_schema.dump(all_favorite_recipe)
    return jsonify(result)
    
# Show one favorite recipe
@app.route('/favorite_recipe', methods=['GET'])
@token_required
def get_favorite_recipe(current_user, favorite_recipe_id):
    favorite_recipe = FavoriteRecipe.query.get_or_404(favorite_recipe_id)
    return favorite_recipe_schema.jsonify(favorite_recipe)

# Delete favorite recipe
@app.route('/favorite_recipe', methods=['DELETE'])
@token_required
def delete_favorite_recipe(current_user, favorite_recipe_id):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    favorite_recipe = FavoriteRecipe.query.get_or_404(favorite_recipe_id)
    db.session.delete(favorite_recipe)
    db.session.commit()
    return '', 204

