import datetime
import json
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from ..common.schemas import products_schema, product_schema
from ..database.models import Product, User, Favorite
from luizalab import db, parser


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