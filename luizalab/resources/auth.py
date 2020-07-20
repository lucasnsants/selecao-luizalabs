import datetime
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token
)
from ..common.schemas import user_schema
from ..database.models import User
from luizalab import db, parser


class Signup(Resource):
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
            


class Signin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {"msg": "Missing email parameter"}, 400
        
        access_token = create_access_token(identity=user_schema.dump(user))
        return { 'access_token': access_token }, 200