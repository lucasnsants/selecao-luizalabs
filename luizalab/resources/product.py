import datetime
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required
)
from ..common.utils import admin_required, doesnt_exist
from ..common.schemas import products_schema, product_schema
from ..database.models import Product
from luizalab import db, parser


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
        return product_schema.dump(product)

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