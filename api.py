from flask import Flask
from config import Config
from models import db, User, Ingredient, init_app

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

# Routes...

