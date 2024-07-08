from ext import app, db
from models import User, Item

with app.app_context():
    db.drop_all()
    db.create_all()
    admin_user = User(username="admin", birthday=datetime.date(1990, 1, 1), gender="MA", country="UK")
    admin_user.set_password("adminpass")
    db.session.add(admin_user)
    db.session.commit()