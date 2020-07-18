import datetime
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, marshal, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import BaseConfig


app = Flask(__name__)
api = Api(app)
app.config.from_object(BaseConfig)
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
        abort(kwargs['status_code'], message="Product {} doesn't exist".format(kwargs['id']))

class ProductList(Resource):
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
    
    def post(self):
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
        return product_schema.dump(new_product)


class ProductId(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        doesnt_exist(obj=product, id=product_id, status_code=404)
        return product_schema.jsonify(product)

    def put(self, product_id):
        product = Product.query.get(product_id)
        doesnt_exist(obj=product, id=product_id, status_code=404)
        new_product = request.get_json()
        product.title = new_product['title']
        product.image = new_product['image']
        product.price = new_product['price']
        product.brand = new_product['brand']
        product.review_score = new_product['review_score']

        db.session.commit()

        return product_schema.jsonify(product)

    def delete(self, product_id):
        product = Product.query.get(product_id)
        doesnt_exist(obj=product, id=product_id, status_code=404)
        db.session.delete(product)
        db.session.commit()
        return 'successful deletion.', 201


api.add_resource(HelloWorld, '/')
api.add_resource(ProductList, '/product/')
api.add_resource(ProductId, '/product/<product_id>')

if __name__ == '__main__':
    app.run(debug=True)
