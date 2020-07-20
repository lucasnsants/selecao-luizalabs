from luizalab import ma


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'image', 'price', 'brand', 'review_score', 'created_at', 'updated_at')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'rule_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)