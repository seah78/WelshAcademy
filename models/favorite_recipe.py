from utils.extensions import db, ma

class FavoriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id

    @classmethod
    def init_app(cls, app):
        with app.app_context():
            db.create_all()

class FavoriteRecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'recipe_id')

favorite_recipe_schema = FavoriteRecipeSchema()
favorites_recipes_schema = FavoriteRecipeSchema(many=True)





