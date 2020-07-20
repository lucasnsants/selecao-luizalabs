import datetime
from luizalab import db
from luizalab.database.models import User

def seed_admin():
    admin = User(name='admin', email='admin@admin.com', rule_id=1, updated_at=datetime.datetime.now())
    db.session.add(admin)
    db.session.commit()