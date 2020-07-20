import datetime
import json
from luizalab import db
from luizalab.database.models import Product

def seedProduct():
    products = []

    with open('data.json') as d:
        data = json.load(d)

    for product in data:
        new_product = Product(title=product['title'], image=product['image'], price=product['price'], 
            brand=product['brand'], review_score=product['review_score'], updated_at=datetime.datetime.now())
        products.append(new_product)

    db.session.add_all(products)
    db.session.commit()