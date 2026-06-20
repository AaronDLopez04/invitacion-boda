from app import create_app
from app import db

app = create_app()

with app.app_context():

    db.drop_all()

    db.create_all()

print("Base recreada correctamente")