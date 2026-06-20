from werkzeug.security import (
    generate_password_hash
)

from app import create_app
from app import db

from app.models.administrador import (
    Administrador
)

app = create_app()

with app.app_context():

    usuario = "magdiel"

    password = generate_password_hash(
        "boda2026"
    )

    admin = Administrador(

        usuario=usuario,

        password=password
    )

    db.session.add(admin)

    db.session.commit()

    print(
        "Administrador creado"
    )