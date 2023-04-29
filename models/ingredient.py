from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# Ingredient model 
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

class IngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


def init_app(app):
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()