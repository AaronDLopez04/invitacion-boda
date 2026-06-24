from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from app import db

from app.models.boda_civil import BodaCivil
from app.models.invitado_civil import InvitadoCivil

from app.utils.auth import login_requerido
from app.utils.helpers import generar_token


admin_civil_bp = Blueprint(
    "admin_civil",
    __name__,
    url_prefix="/admin/civil"
)


def obtener_boda_civil():
    """
    Obtiene la configuración de la boda civil.

    Si todavía no existe un registro,
    lo crea automáticamente.
    """

    boda_civil = BodaCivil.query.first()

    if boda_civil is None:

        boda_civil = BodaCivil(
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

        db.session.add(boda_civil)
        db.session.commit()

    return boda_civil


def generar_token_civil():
    """
    Genera un token que no esté repetido
    entre los invitados civiles.
    """

    token = generar_token()

    while InvitadoCivil.query.filter_by(
        token=token
    ).first():

        token = generar_token()

    return token


@admin_civil_bp.route("/")
@login_requerido
def dashboard():

    boda_civil = obtener_boda_civil()

    busqueda = request.args.get(
        "q",
        ""
    ).strip()

    query = InvitadoCivil.query

    if busqueda:

        query = query.filter(
            InvitadoCivil.nombre.contains(
                busqueda
            )
        )

    invitados = query.order_by(
        InvitadoCivil.nombre
    ).all()

    todos_los_invitados = (
        InvitadoCivil.query.all()
    )

    total_invitados = len(
        todos_los_invitados
    )

    total_pases = sum(
        invitado.pases or 0
        for invitado in todos_los_invitados
    )

    asistentes_confirmados = sum(
        invitado.asistentes_confirmados or 0
        for invitado in todos_los_invitados
    )

    pendientes = InvitadoCivil.query.filter_by(
        respuesta="pendiente"
    ).count()

    no_asistiran = InvitadoCivil.query.filter_by(
        respuesta="no"
    ).count()

    porcentaje = 0

    if total_pases > 0:

        porcentaje = round(
            (
                asistentes_confirmados
                / total_pases
            ) * 100
        )

    return render_template(
        "admin/civil/dashboard.html",
        boda=boda_civil,
        invitados=invitados,
        total_invitados=total_invitados,
        total_pases=total_pases,
        asistentes_confirmados=asistentes_confirmados,
        pendientes=pendientes,
        no_asistiran=no_asistiran,
        porcentaje=porcentaje,
        busqueda=busqueda
    )


@admin_civil_bp.route(
    "/nuevo",
    methods=["GET", "POST"]
)
@login_requerido
def nuevo_invitado():

    error = None

    if request.method == "POST":

        nombre = request.form.get(
            "nombre",
            ""
        ).strip()

        telefono = request.form.get(
            "telefono",
            ""
        ).strip()

        pases_texto = request.form.get(
            "pases",
            "1"
        ).strip()

        if not nombre:

            error = (
                "Debes escribir el nombre "
                "del invitado."
            )

        try:

            pases = int(pases_texto)

        except ValueError:

            pases = 0

        if pases < 1:

            error = (
                "La cantidad de pases debe "
                "ser mayor que cero."
            )

        if error is None:

            invitado = InvitadoCivil(
                nombre=nombre,
                telefono=telefono,
                pases=pases,
                token=generar_token_civil(),
                respuesta="pendiente",
                asistentes_confirmados=0,
                confirmado=False
            )

            db.session.add(invitado)
            db.session.commit()

            return redirect(
                url_for(
                    "admin_civil.dashboard"
                )
            )

    return render_template(
        "admin/civil/nuevo_invitado.html",
        error=error
    )


@admin_civil_bp.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_requerido
def editar_invitado(id):

    invitado = InvitadoCivil.query.get_or_404(
        id
    )

    error = None

    if request.method == "POST":

        nombre = request.form.get(
            "nombre",
            ""
        ).strip()

        telefono = request.form.get(
            "telefono",
            ""
        ).strip()

        pases_texto = request.form.get(
            "pases",
            "1"
        ).strip()

        if not nombre:

            error = (
                "Debes escribir el nombre "
                "del invitado."
            )

        try:

            pases = int(pases_texto)

        except ValueError:

            pases = 0

        if pases < 1:

            error = (
                "La cantidad de pases debe "
                "ser mayor que cero."
            )

        if error is None:

            invitado.nombre = nombre
            invitado.telefono = telefono
            invitado.pases = pases

            if (
                invitado.asistentes_confirmados
                > pases
            ):

                invitado.asistentes_confirmados = (
                    pases
                )

            db.session.commit()

            return redirect(
                url_for(
                    "admin_civil.dashboard"
                )
            )

    return render_template(
        "admin/civil/editar_invitado.html",
        invitado=invitado,
        error=error
    )


@admin_civil_bp.route(
    "/eliminar/<int:id>",
    methods=["POST"]
)
@login_requerido
def eliminar_invitado(id):

    invitado = InvitadoCivil.query.get_or_404(
        id
    )

    db.session.delete(invitado)
    db.session.commit()

    return redirect(
        url_for(
            "admin_civil.dashboard"
        )
    )


@admin_civil_bp.route(
    "/configuracion",
    methods=["GET", "POST"]
)
@login_requerido
def configuracion():

    boda_civil = obtener_boda_civil()

    if request.method == "POST":

        boda_civil.nombre_novia = request.form.get(
            "nombre_novia",
            ""
        ).strip()

        boda_civil.nombre_novio = request.form.get(
            "nombre_novio",
            ""
        ).strip()

        boda_civil.fecha = request.form.get(
            "fecha",
            ""
        ).strip()

        boda_civil.hora = request.form.get(
            "hora",
            ""
        ).strip()

        boda_civil.lugar = request.form.get(
            "lugar",
            ""
        ).strip()

        boda_civil.direccion = request.form.get(
            "direccion",
            ""
        ).strip()

        boda_civil.mapa_url = request.form.get(
            "mapa_url",
            ""
        ).strip()

        boda_civil.mensaje_bienvenida = (
            request.form.get(
                "mensaje_bienvenida",
                ""
            ).strip()
        )

        boda_civil.mesa_regalos = request.form.get(
            "mesa_regalos",
            ""
        ).strip()

        boda_civil.mensaje_mesa_regalos = (
            request.form.get(
                "mensaje_mesa_regalos",
                ""
            ).strip()
        )

        boda_civil.imagen_1 = request.form.get(
            "imagen_1",
            ""
        ).strip()

        boda_civil.imagen_2 = request.form.get(
            "imagen_2",
            ""
        ).strip()

        boda_civil.imagen_3 = request.form.get(
            "imagen_3",
            ""
        ).strip()

        boda_civil.imagen_4 = request.form.get(
            "imagen_4",
            ""
        ).strip()

        boda_civil.imagen_5 = request.form.get(
            "imagen_5",
            ""
        ).strip()

        db.session.commit()

        return redirect(
            url_for(
                "admin_civil.configuracion",
                guardado="1"
            )
        )

    guardado = (
        request.args.get("guardado")
        == "1"
    )

    return render_template(
        "admin/civil/configuracion.html",
        boda=boda_civil,
        guardado=guardado
    )