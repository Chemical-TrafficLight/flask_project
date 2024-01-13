from app import db, app
from models import User
from werkzeug.security import generate_password_hash

new_user = User(name="admin", email="admin@gmail.com", password=generate_password_hash("admin"), role=1)
with app.app_context():
    db.session.add(new_user)
    db.session.commit()