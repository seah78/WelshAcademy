from utils.extensions import db, ma

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

    @classmethod
    def init_app(cls, app):
        with app.app_context():
            db.create_all()

class RecipeIngredientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'recipe_id', 'ingredient_id', 'quantity')

recipe_ingredient_schema = RecipeIngredientSchema()
recipe_ingredients_schema = RecipeIngredientSchema(many=True)

