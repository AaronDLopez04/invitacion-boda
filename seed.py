from app import create_app
from app import db

from app.models.boda import Boda


app = create_app()


with app.app_context():

    db.create_all()

    boda = Boda.query.first()

    if boda is None:

        boda = Boda(

            nombre_novia="Eunice",

            nombre_novio="Magdiel",

            fecha="2026-12-05",

            hora="2:30 PM",

            lugar_ceremonia="Campamento Citlali (Compañerismo Estudiantil A. C.), Avándaro, Valle de Bravo, Estado de México",

            direccion_ceremonia="https://maps.app.goo.gl/bHyiBGA8YADikKUS6",

            codigo_vestimenta="https://mx.pinterest.com/adanylg2004/boda-eunice-y-magdiel/",

            versiculo="Isaías 41:20",

            historia="""Con Su infinita gracia unió lo incompatible, trazó nuestro destino y entrelazó nuestros días.

Desde nuestros primeros pasos en la preparatoria hasta cruzar la meta de la universidad, Su amor nos ha guiado.

Él: «Me cautivó el brillo de su sonrisa y su corazón dispuesto a servir a Dios.»

Ella: «Me enamoraron sus ojos y la profundidad de su conexión con el Creador.»

Hoy, guiados por la fe, decidimos amarnos frente a cualquier circunstancia, con la firme certeza de que no hay fuerza en este mundo que nos pueda separar.""",

            mensaje_bienvenida="Nos sentimos muy felices de poder celebrar este día tan especial contigo.",

            mesa_regalos="https://www.amazon.com.mx/wedding/guest-view/3RMIP8SGYVHJM",

            hospedaje="Para hospedaje comunicarse al +52 1 55 5973 8124",

            whatsapp_novio="+5215546864443",

            whatsapp_novia="+5215572146656",

            whatsapp_hospedaje="+5215559738124"

        )

        db.session.add(
            boda
        )

        db.session.commit()

        print(
            "Datos de la boda cargados correctamente."
        )

    else:

        print(
            "La información de la boda ya existe."
        )