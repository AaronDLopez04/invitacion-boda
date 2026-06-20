from app import db


class Mesa(db.Model):

    __tablename__ = "mesas"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    capacidad = db.Column(db.Integer, nullable=False, default=10)

    pos_x = db.Column(
        db.Integer,
        default=0
    )

    pos_y = db.Column(
        db.Integer,
        default=0
    )

    invitados = db.relationship(
        "Invitado",
        backref="mesa",
        lazy=True
    )