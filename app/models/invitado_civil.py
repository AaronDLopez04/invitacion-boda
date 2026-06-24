from app import db


class InvitadoCivil(db.Model):

    __tablename__ = "invitados_civiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    telefono = db.Column(
        db.String(30),
        nullable=True
    )

    pases = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    token = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    respuesta = db.Column(
        db.String(20),
        nullable=False,
        default="pendiente"
    )

    asistentes_confirmados = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    comentarios = db.Column(
        db.Text,
        nullable=True
    )

    confirmado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    fecha_confirmacion = db.Column(
        db.String(30),
        nullable=True
    )

    def __repr__(self):

        return (
            f"<InvitadoCivil "
            f"{self.nombre}>"
        )