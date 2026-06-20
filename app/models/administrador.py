from app import db


class Administrador(db.Model):

    __tablename__ = "administradores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )