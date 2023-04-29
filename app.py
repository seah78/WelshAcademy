from flask import Flask, request, jsonify
import jwt
from functools import wraps

from config import Config
from api.user import user_api
from api.ingredient import ingredient_api
from api.recipe import recipe_api
from api.recipeingredient import recipe_ingredient_api
from api.favoriterecipe import favorite_recipe_api
from models.user import User, init_app

app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(ingredient_api)
app.register_blueprint(recipe_api)
app.register_blueprint(recipe_ingredient_api)
app.register_blueprint(favorite_recipe_api)

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