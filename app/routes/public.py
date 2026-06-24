from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for

from app.models.invitado import Invitado

public_bp = Blueprint(
    "public",
    __name__
)


@public_bp.route("/")
def inicio():

    return render_template(
        "public/index.html"
    )


@public_bp.route("/invitacion")
def invitacion():

    invitado = Invitado.query.first()

    if not invitado:

        return render_template(
    "errors/invitacion_no_disponible.html"
), 404

    return redirect(
        url_for(
            "invitados.invitacion_personalizada",
            token=invitado.token
        )
    )