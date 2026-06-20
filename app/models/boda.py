from app import db


class Boda(db.Model):

    __tablename__ = "boda"

    id = db.Column(db.Integer, primary_key=True)

    nombre_novia = db.Column(db.String(100), nullable=False)
    nombre_novio = db.Column(db.String(100), nullable=False)

    fecha = db.Column(db.String(30), nullable=False)
    hora = db.Column(db.String(20), nullable=False)

    versiculo = db.Column(db.String(100))

    mensaje_bienvenida = db.Column(db.Text)
    historia = db.Column(db.Text)

    lugar_ceremonia = db.Column(db.String(300))
    direccion_ceremonia = db.Column(db.String(500))

    codigo_vestimenta = db.Column(db.String(200))

    mesa_regalos = db.Column(db.String(500))
    hospedaje = db.Column(db.Text)

    whatsapp_novio = db.Column(db.String(30))
    whatsapp_novia = db.Column(db.String(30))
    whatsapp_hospedaje = db.Column(db.String(30))