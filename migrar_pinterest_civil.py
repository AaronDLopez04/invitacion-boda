from sqlalchemy import text

from app import create_app
from app import db


app = create_app()

with app.app_context():

    print("Conectando con la base de datos...")

    db.session.execute(
        text(
            """
            ALTER TABLE bodas_civiles
            ADD COLUMN IF NOT EXISTS pinterest_url VARCHAR(500);
            """
        )
    )

    db.session.commit()

    print(
        "La columna 'pinterest_url' "
        "se agregó correctamente."
    )