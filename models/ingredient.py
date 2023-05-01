from utils.extensions import db, ma

# Ingredient model 
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

    @classmethod
    def init_app(cls, app):
        with app.app_context():
            db.create_all()
            
class IngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

