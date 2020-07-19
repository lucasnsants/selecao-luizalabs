import datetime
from app import db
from models import User

def seed_user():
    admin = User(name='Test Product', email='product@test.com', rule_id=1, updated_at=datetime.datetime.now())
    db.session.add(admin)
    db.session.commit()