from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from datetime import datetime

from app import db

from app.models.boda import Boda
from app.models.invitado import Invitado

invitados_bp = Blueprint(
    "invitados",
    __name__
)


@invitados_bp.route(
    "/i/<token>"
)
def invitacion_personalizada(token):

    boda = Boda.query.first()

    invitado = Invitado.query.filter_by(
        token=token
    ).first()

    if not invitado:

        return "Invitación no encontrada", 404

    spotify_embed = None

    if boda and boda.spotify_url:

        spotify_embed = (
            boda.spotify_url
            .replace(
                "open.spotify.com/",
                "open.spotify.com/embed/"
            )
            .split("?")[0]
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

    if not invitado:

        return "Invitación no encontrada", 404

    respuesta = request.form.get(
        "respuesta"
    )

    asistentes = request.form.get(
        "asistentes"
    )

    comentarios = request.form.get(
        "comentarios"
    )

    invitado.respuesta = respuesta

    invitado.asistentes_confirmados = int(
        asistentes
    )

    invitado.comentarios = comentarios

    invitado.confirmado = (
        respuesta == "si"
    )

    invitado.fecha_confirmacion = (
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    db.session.commit()

    return redirect(
        url_for(
            "invitados.invitacion_personalizada",
            token=token
        )
    )