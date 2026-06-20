from app import create_app
from app import db

from app.models.invitado import Invitado


app = create_app()


with app.app_context():

    if Invitado.query.count() == 0:

        invitados = [

            Invitado(
                nombre="Familia López Hernández",
                telefono="5555555555",
                pases=4,
                token="ABC123"
            ),

            Invitado(
                nombre="Juan Pérez",
                telefono="5555555555",
                pases=2,
                token="XYZ789"
            )

        ]

        db.session.add_all(
            invitados
        )

        db.session.commit()

        print(
            "Invitados de prueba cargados correctamente."
        )

    else:

        print(
            "Ya existen invitados. No se cargaron datos de prueba."
        )