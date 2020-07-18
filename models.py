import datetime
from app import db


favorites = db.Table('favorites', 
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=False)
    favorites = db.relationship('Product', secondary=favorites, lazy='subquery', backref=db.backref('users', lazy=True))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, email, rule_id, updated_at):
        self.name = name
        self.email = email
        self.rule_id = rule_id
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def __repr__(self):
        return '<User %r>' % self.name

class Rule(db.Model):
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', backref='rules', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, updated_at):
        self.name = name
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def __repr__(self):
        return '<Rule %r>' % self.name

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    review_score = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, image, price, brand, review_score, updated_at):
        self.title = title
        self.image = image
        self.price = price
        self.brand = brand
        self.review_score = review_score
        self.created_at = datetime.datetime.now()
        self.updated_at = updated_at

    def __repr__(self):
        return '<Produt %r>' % self.title