from datetime import datetime

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from app import db
from app.models.boda_civil import BodaCivil
from app.models.invitado_civil import InvitadoCivil
from app.utils.helpers import generar_token


civil_bp = Blueprint(
    "civil",
    __name__,
    url_prefix="/civil"
)


MESES_ES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"
]


def obtener_boda_civil():

    boda = BodaCivil.query.first()

    if boda is None:

        boda = BodaCivil(
            nombre_novia="Eunice",
            nombre_novio="Magdiel",
            mensaje_bienvenida=(
                "Nos llena de alegría compartir contigo "
                "este momento tan especial."
            ),
            mensaje_mesa_regalos=(
                "Tu presencia es nuestro mejor regalo."
            ),
            imagen_1="civil-1.jpg",
            imagen_2="civil-2.jpg",
            imagen_3="civil-3.jpg"
        )

        db.session.add(boda)
        db.session.commit()

    return boda


def generar_token_civil():

    token = generar_token()

    while InvitadoCivil.query.filter_by(
        token=token
    ).first():

        token = generar_token()

    return token


def obtener_imagenes(boda):

    imagenes = [
        boda.imagen_1,
        boda.imagen_2,
        boda.imagen_3,
        boda.imagen_4,
        boda.imagen_5
    ]

    return [
        imagen.strip()
        for imagen in imagenes
        if imagen and imagen.strip()
    ]


def formatear_fecha(fecha):

    if not fecha:

        return ""

    try:

        fecha_objeto = datetime.strptime(
            fecha,
            "%Y-%m-%d"
        )

        return (
            f"{fecha_objeto.day} de "
            f"{MESES_ES[fecha_objeto.month - 1]} de "
            f"{fecha_objeto.year}"
        )

    except ValueError:

        return fecha


def formatear_hora(hora):

    if not hora:

        return ""

    try:

        hora_objeto = datetime.strptime(
            hora,
            "%H:%M"
        )

        hora_formateada = hora_objeto.strftime(
            "%I:%M %p"
        ).lstrip("0")

        return (
            hora_formateada
            .replace("AM", "a. m.")
            .replace("PM", "p. m.")
        )

    except ValueError:

        return hora


@civil_bp.route("/")
def invitacion_general():

    boda = obtener_boda_civil()

    return render_template(
        "public/invitacion_civil_general.html",
        boda=boda,
        imagenes=obtener_imagenes(boda),
        fecha_legible=formatear_fecha(
            boda.fecha
        ),
        hora_legible=formatear_hora(
            boda.hora
        )
    )


@civil_bp.route(
    "/registrar",
    methods=["POST"]
)
def registrar_invitado():

    boda = obtener_boda_civil()

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()

    telefono = request.form.get(
        "telefono",
        ""
    ).strip()

    comentarios = request.form.get(
        "comentarios",
        ""
    ).strip()

    if not nombre:

        return redirect(
            url_for(
                "civil.invitacion_general"
            )
        )

    invitado = InvitadoCivil(
        nombre=nombre,
        telefono=telefono,
        pases=1,
        token=generar_token_civil(),
        respuesta="si",
        asistentes_confirmados=1,
        comentarios=comentarios,
        confirmado=True,
        fecha_confirmacion=datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    db.session.add(invitado)
    db.session.commit()

    return redirect(
        url_for(
            "civil.invitacion",
            token=invitado.token,
            registrado="1"
        )
    )


@civil_bp.route("/<token>")
def invitacion(token):

    invitado = InvitadoCivil.query.filter_by(
        token=token
    ).first()

    if invitado is None:

        return render_template(
            "errors/invitacion_no_disponible.html"
        ), 404

    boda = obtener_boda_civil()

    confirmacion_guardada = (
        request.args.get("confirmado") == "1"
    )

    registro_guardado = (
        request.args.get("registrado") == "1"
    )

    return render_template(
        "public/invitacion_civil.html",
        boda=boda,
        invitado=invitado,
        imagenes=obtener_imagenes(boda),
        fecha_legible=formatear_fecha(
            boda.fecha
        ),
        hora_legible=formatear_hora(
            boda.hora
        ),
        confirmacion_guardada=confirmacion_guardada,
        registro_guardado=registro_guardado
    )


@civil_bp.route(
    "/confirmar/<token>",
    methods=["POST"]
)
def confirmar(token):

    invitado = InvitadoCivil.query.filter_by(
        token=token
    ).first()

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
                "civil.invitacion",
                token=token
            )
        )

    if respuesta == "si":

        invitado.confirmado = True
        invitado.asistentes_confirmados = 1

    else:

        invitado.confirmado = False
        invitado.asistentes_confirmados = 0

    invitado.pases = 1
    invitado.respuesta = respuesta
    invitado.comentarios = comentarios

    invitado.fecha_confirmacion = (
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    db.session.commit()

    return redirect(
        url_for(
            "civil.invitacion",
            token=token,
            confirmado="1"
        )
    )