import datetime
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, marshal, reqparse, abort
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
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


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'image', 'price', 'brand', 'review_score', 'created_at', 'updated_at')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}

def doesnt_exist(**kwargs):
    if kwargs['obj'] is None:
        abort(kwargs['status_code'], msg="{} doesn't exist".format(kwargs['id']))


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

            access_token = create_access_token(identity=new_user.email)

            return { 'access_token': access_token }, 201
        except Exception as exc:
            return jsonify(exc), 500
            


class Auth(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {"msg": "Missing email parameter"}, 400
        
        access_token = create_access_token(identity=user.email)
        return { 'access_token': access_token }, 200

class ProductList(Resource):
    @jwt_required
    def get(self):
        args = parser.parse_args()
        products = Product.query.order_by(Product.created_at.desc()).paginate(page=args['page'], per_page=args['limit'], error_out=False)
        total_count = Product.query.count()
        result = products_schema.dump(products.items)
        return jsonify({
            'list': result,
            'page': args['page'],
            'to_page': args['page'] + 1,
            'page_size': args['limit'],
            'total_count': total_count
        })
    
    @jwt_required
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

    @jwt_required
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

    @jwt_required
    def delete(self, product_id):
        try:
            product = Product.query.get(product_id)
            doesnt_exist(obj=product, id=product_id, status_code=404)
            db.session.delete(product)
            db.session.commit()
            return { 'msg': 'successful deletion.' }, 201
        except Exception as exc:
            return jsonify(exc), 500


api.add_resource(HelloWorld, '/')
api.add_resource(ProductList, '/product/')
api.add_resource(ProductId, '/product/<product_id>')

api.add_resource(Auth, '/auth/login')
api.add_resource(Register, '/auth/register')

if __name__ == '__main__':
    app.run(debug=True)
