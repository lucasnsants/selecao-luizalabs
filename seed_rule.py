import datetime
from app import db
from models import Rule

def seed_rule():
    rule_admin = Rule(name='admin', updated_at=datetime.datetime.now())
    rule_user = Rule(name='user', updated_at=datetime.datetime.now())
    db.session.add(rule_admin)
    db.session.add(rule_user)
    db.session.commit()