import os

from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for

from werkzeug.utils import secure_filename

from app import db

from app.models.boda import Boda
from app.models.invitado import Invitado

from app.services.qr_service import generar_credencial_qr


invitados_bp = Blueprint(
    "invitados",
    __name__
)


def obtener_spotify_embed(spotify_url):
    """
    Convierte un enlace normal de Spotify
    en un enlace compatible con iframe.
    """

    if not spotify_url:

        return None

    spotify_url = spotify_url.strip()

    if "open.spotify.com/embed/" in spotify_url:

        return spotify_url.split("?")[0]

    return (
        spotify_url
        .replace(
            "open.spotify.com/",
            "open.spotify.com/embed/"
        )
        .split("?")[0]
    )


def generar_pase_invitado(
    invitado,
    boda
):
    """
    Genera nuevamente el pase QR del invitado.

    Esto permite recuperar el archivo aunque
    Render haya reiniciado su almacenamiento local.
    """

    url_invitacion = url_for(
        "invitados.invitacion_personalizada",
        token=invitado.token,
        _external=True
    )

    generar_credencial_qr(
        invitado,
        boda,
        url_invitacion
    )


@invitados_bp.route(
    "/i/<token>"
)
def invitacion_personalizada(token):

    invitado = Invitado.query.filter_by(
        token=token
    ).first()

    if invitado is None:

        return render_template(
        "errors/invitacion_no_disponible.html"
    ), 404

    boda = Boda.query.first()

    if invitado is None:

        return render_template(
        "errors/invitacion_no_disponible.html"
    ), 404

    spotify_embed = obtener_spotify_embed(
        boda.spotify_url
    )

    return render_template(
        "public/invitacion_personalizada.html",
        boda=boda,
        invitado=invitado,
        spotify_embed=spotify_embed
    )


@invitados_bp.route(
    "/confirmar/<token>",
    methods=["POST"]
)
def confirmar_asistencia(token):

    invitado = Invitado.query.filter_by(
        token=token
    ).first()

    if invitado is None:

        return render_template(
        "errors/invitacion_no_disponible.html"
    ), 404

    boda = Boda.query.first()

    if invitado is None:

        return render_template(
        "errors/invitacion_no_disponible.html"
    ), 404

    respuesta = request.form.get(
        "respuesta",
        ""
    ).strip().lower()

    comentarios = request.form.get(
        "comentarios",
        ""
    ).strip()

    if respuesta not in [
        "si",
        "no"
    ]:

        return redirect(
            url_for(
                "invitados.invitacion_personalizada",
                token=token
            )
        )

    if respuesta == "si":

        asistentes_texto = request.form.get(
            "asistentes",
            "1"
        )

        try:

            asistentes = int(
                asistentes_texto
            )

        except (TypeError, ValueError):

            asistentes = 1

        asistentes = max(
            1,
            min(
                asistentes,
                invitado.pases
            )
        )

        invitado.confirmado = True
        invitado.asistentes_confirmados = (
            asistentes
        )

    else:

        invitado.confirmado = False
        invitado.asistentes_confirmados = 0

    invitado.respuesta = respuesta
    invitado.comentarios = comentarios

    invitado.fecha_confirmacion = (
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    db.session.commit()

    if respuesta == "si":

        generar_pase_invitado(
            invitado,
            boda
        )

    return redirect(
        url_for(
            "invitados.invitacion_personalizada",
            token=token
        )
    )


@invitados_bp.route(
    "/pase/<token>/descargar"
)
def descargar_pase(token):

    invitado = Invitado.query.filter_by(
        token=token
    ).first()

    if invitado is None:

        return render_template(
        "errors/invitacion_no_disponible.html"
    ), 404

    if invitado.respuesta != "si":

        return redirect(
            url_for(
                "invitados.invitacion_personalizada",
                token=token
            )
        )

    boda = Boda.query.first()

    if invitado is None:

        return render_template(
        "errors/invitacion_no_disponible.html"
    ), 404

    generar_pase_invitado(
        invitado,
        boda
    )

    ruta_archivo = os.path.join(
        current_app.static_folder,
        "qr",
        f"{invitado.token}.png"
    )

    if not os.path.exists(
        ruta_archivo
    ):

        return render_template(
            "errors/404.html"
        ), 404

    nombre_invitado = secure_filename(
        invitado.nombre
    ) or "invitado"

    return send_file(
        ruta_archivo,
        as_attachment=True,
        download_name=(
            f"pase-boda-{nombre_invitado}.png"
        ),
        mimetype="image/png"
    )