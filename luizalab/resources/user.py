import datetime
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required
)
from ..common.utils import admin_required, doesnt_exist
from ..common.schemas import user_schema, users_schema
from ..database.models import User
from luizalab import db, parser


class UserList(Resource):
    @admin_required
    def get(self):
        args = parser.parse_args()
        query = User.query.order_by(User.created_at.desc())
        users = query.paginate(page=args['page'], per_page=args['limit'], error_out=False)
        total_count = query.count()
        result = users_schema.dump(users.items)
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