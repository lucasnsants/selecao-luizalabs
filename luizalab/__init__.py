from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (
    JWTManager
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


parser = reqparse.RequestParser()
parser.add_argument('page', default=1, type=int)
parser.add_argument('limit', default=10, type=int)
parser.add_argument('product_id', type=int)


from .common.utils import doesnt_exist, admin_required
from .common.schemas import products_schema, product_schema, user_schema
from .resources.version import VersionAPI
from .resources.auth import Signin, Signup
from .resources.product import ProductList, ProductId
from .resources.user import UserList, UserId
from .resources.favorite import FavoriteList


api.add_resource(VersionAPI, '/')

api.add_resource(Signin, '/v1/signin')
api.add_resource(Signup, '/v1/signup')

api.add_resource(UserList, '/v1/users/')
api.add_resource(UserId, '/v1/user/', '/v1/user/<user_id>')

api.add_resource(ProductList, '/v1/product/')
api.add_resource(ProductId, '/v1/product/<product_id>')

api.add_resource(FavoriteList, '/v1/favorite/')