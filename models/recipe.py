from utils.extensions import db, ma


# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    ingredients = db.relationship("RecipeIngredient", backref="recipe", lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def init_app(cls, app):
        with app.app_context():
            db.create_all()


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "ingredients")


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)
