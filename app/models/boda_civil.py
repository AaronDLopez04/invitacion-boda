from app import db


class BodaCivil(db.Model):

    __tablename__ = "bodas_civiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre_novia = db.Column(
        db.String(120),
        nullable=False,
        default="Eunice"
    )

    nombre_novio = db.Column(
        db.String(120),
        nullable=False,
        default="Magdiel"
    )

    fecha = db.Column(
        db.String(30),
        nullable=True
    )

    hora = db.Column(
        db.String(30),
        nullable=True
    )

    lugar = db.Column(
        db.String(250),
        nullable=True
    )

    direccion = db.Column(
        db.Text,
        nullable=True
    )

    mapa_url = db.Column(
        db.String(500),
        nullable=True
    )

    mensaje_bienvenida = db.Column(
        db.Text,
        nullable=True
    )

    mesa_regalos = db.Column(
        db.String(500),
        nullable=True
    )

    mensaje_mesa_regalos = db.Column(
        db.Text,
        nullable=True
    )

    # Nombres de los archivos que formarán el carrusel.
    # Las imágenes estarán en app/static/img/civil/
    imagen_1 = db.Column(
        db.String(255),
        nullable=True,
        default="civil-1.jpg"
    )

    imagen_2 = db.Column(
        db.String(255),
        nullable=True,
        default="civil-2.jpg"
    )

    imagen_3 = db.Column(
        db.String(255),
        nullable=True,
        default="civil-3.jpg"
    )

    imagen_4 = db.Column(
        db.String(255),
        nullable=True
    )

    imagen_5 = db.Column(
        db.String(255),
        nullable=True
    )

    def __repr__(self):

        return (
            f"<BodaCivil "
            f"{self.nombre_novia} y "
            f"{self.nombre_novio}>"
        )