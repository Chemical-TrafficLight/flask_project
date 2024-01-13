from app import app
from models import db, Products

for i in range(1, 10):
    product1 = Products(name=f"Краски{i}", price=str(100 + i))
    with app.app_context():
        db.session.add(product1)
        db.session.commit()