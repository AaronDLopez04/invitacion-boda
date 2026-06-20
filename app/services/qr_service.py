import os
import qrcode

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from flask import current_app


def generar_credencial_qr(invitado, boda, url_invitacion):

    carpeta_qr = os.path.join(
        current_app.root_path,
        "static",
        "qr"
    )

    os.makedirs(
        carpeta_qr,
        exist_ok=True
    )

    nombre_archivo = f"{invitado.token}.png"

    ruta_final = os.path.join(
        carpeta_qr,
        nombre_archivo
    )

    qr = qrcode.make(
        url_invitacion
    ).resize(
        (420, 420)
    )

    ancho = 900
    alto = 1300

    imagen = Image.new(
        "RGB",
        (ancho, alto),
        "#F8F4F1"
    )

    draw = ImageDraw.Draw(imagen)

    color_texto = "#403A36"
    color_detalle = "#B59673"

    try:
        fuente_titulo = ImageFont.truetype(
            "arial.ttf",
            70
        )

        fuente_subtitulo = ImageFont.truetype(
            "arial.ttf",
            38
        )

        fuente_texto = ImageFont.truetype(
            "arial.ttf",
            32
        )

    except:

        fuente_titulo = ImageFont.load_default()
        fuente_subtitulo = ImageFont.load_default()
        fuente_texto = ImageFont.load_default()

    draw.rounded_rectangle(
        (60, 60, ancho - 60, alto - 60),
        radius=35,
        fill="white",
        outline=color_detalle,
        width=4
    )

    draw.text(
        (ancho / 2, 150),
        f"{boda.nombre_novia} & {boda.nombre_novio}",
        fill=color_texto,
        font=fuente_titulo,
        anchor="mm"
    )

    draw.text(
        (ancho / 2, 240),
        "INVITACIÓN",
        fill=color_detalle,
        font=fuente_subtitulo,
        anchor="mm"
    )

    imagen.paste(
        qr,
        (
            int((ancho - 420) / 2),
            330
        )
    )

    draw.text(
        (ancho / 2, 820),
        invitado.nombre,
        fill=color_texto,
        font=fuente_subtitulo,
        anchor="mm"
    )

    draw.text(
        (ancho / 2, 900),
        f"Invitación válida para {invitado.pases} personas",
        fill=color_texto,
        font=fuente_texto,
        anchor="mm"
    )

    draw.text(
        (ancho / 2, 980),
        boda.fecha,
        fill=color_detalle,
        font=fuente_texto,
        anchor="mm"
    )

    draw.text(
        (ancho / 2, 1060),
        f"Token: {invitado.token}",
        fill=color_texto,
        font=fuente_texto,
        anchor="mm"
    )

    draw.text(
        (ancho / 2, 1170),
        "Con amor, Eunice & Magdiel",
        fill=color_detalle,
        font=fuente_texto,
        anchor="mm"
    )

    imagen.save(
        ruta_final
    )

    return nombre_archivo