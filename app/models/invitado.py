from app import db


class Invitado(db.Model):

    __tablename__ = "invitados"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(200),
        nullable=False
    )

    telefono = db.Column(
        db.String(20)
    )

    pases = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    token = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    confirmado = db.Column(
        db.Boolean,
        default=False
    )

    comentarios = db.Column(
        db.Text
    )

    fecha_confirmacion = db.Column(
        db.String(50)
    )

    respuesta = db.Column(
        db.String(20),
        default="pendiente"
    )

    asistentes_confirmados = db.Column(
        db.Integer,
        default=0
    )

    mesa_id = db.Column(
        db.Integer,
        db.ForeignKey("mesas.id"),
        nullable=True
    )

    personas_ingresadas = db.Column(
        db.Integer,
        default=0
    )

    hora_ingreso = db.Column(
        db.String(50)
    )

    checkin_completo = db.Column(
        db.Boolean,
        default=False
    )