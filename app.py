import datetime
import json
from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, marshal, reqparse, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, verify_jwt_in_request, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import BaseConfig


app = Flask(__name__)
api = Api(app)
app.config.from_object(BaseConfig)
jwt = JWTManager(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import *

parser = reqparse.RequestParser()
parser.add_argument('page', default=1, type=int)
parser.add_argument('limit', default=10, type=int)
parser.add_argument('product_id', type=int)


def doesnt_exist(**kwargs):
    if kwargs['obj'] == None:
        print(kwargs['obj'])
        abort(kwargs['status_code'], msg="{} doesn't exist".format(kwargs['id']))

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return { 'msg': 'Admins only!' }, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    if identity['rule_id'] == 1:
        return {'roles': 'admin'}
    else:
        return {'roles': 'peasant'}


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'image', 'price', 'brand', 'review_score', 'created_at', 'updated_at')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'rule_id')

user_schema = UserSchema()


class HelloWorld(Resource):
    def get(self):
        return {'version': '1.0.0'}

class Register(Resource):
    def post(self):
        user = request.get_json()
        if not user:
            return { "msg": "Registration data was not informed." }, 400
        result = User.query.filter_by(email=user['email']).first()
        if result is not None:
            return { "msg": "User already exists" }, 409
        try:
            name = user['name']
            email = user['email']
            rule_id = user['rule_id']
            updated_at = datetime.datetime.now()
            new_user = User(name=name, email=email, rule_id=rule_id, updated_at=updated_at)

            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=user_schema.dump(user))

            return { 'access_token': access_token }, 201
        except Exception as exc:
            return jsonify(exc), 500
            


class Auth(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {"msg": "Missing email parameter"}, 400
        
        access_token = create_access_token(identity=user_schema.dump(user))
        return { 'access_token': access_token }, 200

class ProductList(Resource):
    @jwt_required
    def get(self):
        args = parser.parse_args()
        query = Product.query.order_by(Product.created_at.desc())
        products = query.paginate(page=args['page'], per_page=args['limit'], error_out=False)
        total_count = query.count()
        result = products_schema.dump(products.items)
        return jsonify({
            'list': result,
            'page': args['page'],
            'to_page': args['page'] + 1,
            'page_size': args['limit'],
            'total_count': total_count
        })
    
    @admin_required
    def post(self):
        try:
            product = request.get_json()
            title = product['title']
            image = product['image']
            price = product['price']
            brand = product['brand']
            review_score = product['review_score']
            updated_at = datetime.datetime.now()
            new_product = Product(title, image, price, brand, review_score, updated_at)
            db.session.add(new_product)
            db.session.commit()
            return product_schema.dump(new_product), 201
        except Exception as exc:
            return jsonify(exc), 500


class ProductId(Resource):
    @jwt_required
    def get(self, product_id):
        product = Product.query.get(product_id)
        doesnt_exist(obj=product, id=product_id, status_code=404)
        return product_schema.jsonify(product)

    @admin_required
    def put(self, product_id):
        try:
            product = Product.query.get(product_id)
            doesnt_exist(obj=product, id=product_id, status_code=404)
            new_product = request.get_json()
            product.title = new_product['title']
            product.image = new_product['image']
            product.price = new_product['price']
            product.brand = new_product['brand']
            product.review_score = new_product['review_score']
            product.updated_at = datetime.datetime.now()

            db.session.commit()

            return product_schema.jsonify(product)
        except Exception as exc:
            return jsonify(exc), 500

    @admin_required
    def delete(self, product_id):
        try:
            product = Product.query.get(product_id)
            doesnt_exist(obj=product, id=product_id, status_code=404)
            db.session.delete(product)
            db.session.commit()
            return { 'msg': 'successful deletion.' }, 201
        except Exception as exc:
            return jsonify(exc), 500


class UserList(Resource):
    @admin_required
    def get(self):
        args = parser.parse_args()
        query = User.query.order_by(User.created_at.desc())
        users = query.paginate(page=args['page'], per_page=args['limit'], error_out=False)
        total_count = query.count()
        return jsonify({
            'list': user_schema.dump(users),
            'page': args['page'],
            'to_page': args['page'] + 1,
            'page_size': args['limit'],
            'total_count': total_count
        })

    @admin_required
    def post(self):
        try:
            data = request.get_json()
            name = data['name']
            email = data['email']
            rule_id = data['rule_id']
            updated_at = datetime.datetime.now()

            user = User(name=name, email=email, rule_id=rule_id, updated_at=updated_at)

            db.session.add(user)
            db.session.commit()

            return user_schema.dump(user), 201
        except Exception as exc:
            return jsonify(exc), 500

class UserId(Resource):
    @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        doesnt_exist(obj=user, id=user_id, status_code=404)
        return user_schema.jsonify(user)

    @jwt_required
    def put(self, user_id):
        try:
            user = User.query.get(user_id)
            data = request.get_json()
            user['name'] = data['name']
            user['email'] = data['email']
            user['rule_id'] = data['rule_id']
            user['updated_at'] = datetime.datetime.now()

            db.session.commit()

            return user_schema.dump(user), 201
        except Exception as exc:
            return jsonify(exc), 500

    @jwt_required
    def delete(self, user_id):
        try:
            user = User.query.get(user_id)
            doesnt_exist(obj=user, id=user_id, status_code=404)
            db.session.delete(user)
            db.session.commit()
            return { 'msg': 'successful deletion.' }, 201
        except Exception as exc:
            return jsonify(exc), 500


class FavoriteList(Resource):
    @jwt_required
    def get(self):
        args = parser.parse_args()
        current_user = get_jwt_identity()
        print(current_user['id'])
        query = Product.query.join(Product, User.products).filter(User.id == current_user['id'])
        favorites = query.paginate(page=args['page'], per_page=args['limit'], error_out=False)
        total_count = query.count()
        return jsonify({
            'list': products_schema.dump(favorites.items),
            'page': args['page'],
            'to_page': args['page'] + 1,
            'page_size': args['limit'],
            'total_count': total_count
        })

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        product_id = request.get_json().get('product_id')
        product = Product.query.get(product_id)
        query = Product.query.join(Product.users).filter(User.id == current_user['id'], Product.id == product_id)
        if product == None:
            return { "msg": "Product not found." }, 404
        
        duplicate = query.first()
        if duplicate is not None:
            return { "msg": "Product duplicate." }, 409
        try:
            favorite = Favorite(product_id=product_id, user_id=current_user['id'])
            db.session.add(favorite)
            db.session.commit()
            product = query.first()
            return product_schema.dump(product), 201
        except Exception as exc:
            return json.dumps(exc), 500

    @jwt_required
    def delete(self):
        try:
            current_user = get_jwt_identity()
            product_id = request.get_json().get('product_id')
            favorite = Favorite.query.filter_by(product_id=product_id, user_id=current_user['id']).first()
            db.session.delete(favorite)
            db.session.commit()

            return { 'msg': 'successful deletion.' }, 201
        except Exception as exc:
            return jsonify(exc)


api.add_resource(HelloWorld, '/')
api.add_resource(ProductList, '/v1/product/')
api.add_resource(ProductId, '/v1/product/<product_id>')

api.add_resource(Auth, '/v1/signin')
api.add_resource(Register, '/v1/signup')

api.add_resource(UserList, '/v1/users/')
api.add_resource(UserId, '/v1/user/', '/v1/user/<user_id>')

api.add_resource(FavoriteList, '/v1/favorite/')

if __name__ == '__main__':
    app.run(debug=True)
