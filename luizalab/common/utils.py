from functools import wraps
from flask_restful import abort
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)
from luizalab import jwt

def doesnt_exist(**kwargs):
    if kwargs['obj'] == None:
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