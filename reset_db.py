from app import create_app
from app import db


app = create_app()


with app.app_context():

    database_uri = app.config.get(
        "SQLALCHEMY_DATABASE_URI",
        ""
    )

    # Por seguridad, solo permitimos reiniciar SQLite.
    if not database_uri.startswith("sqlite"):

        print("")
        print("OPERACIÓN CANCELADA")
        print(
            "reset_db.py solamente puede ejecutarse "
            "con una base de datos SQLite local."
        )
        print(
            "La base de datos PostgreSQL de producción "
            "no fue modificada."
        )
        print("")

        raise SystemExit(1)

    confirmacion = input(
        "Esto eliminará la base de datos local. "
        "Escribe REINICIAR para continuar: "
    )

    if confirmacion != "REINICIAR":

        print("Operación cancelada.")

        raise SystemExit(0)

    db.drop_all()
    db.create_all()

    print("")
    print("Base de datos SQLite local reiniciada correctamente.")