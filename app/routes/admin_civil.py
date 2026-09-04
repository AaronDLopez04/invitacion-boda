from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import pandas as pd

from app import db
from app.models.boda_civil import BodaCivil
from app.models.invitado_civil import InvitadoCivil
from app.utils.auth import login_requerido
from app.utils.helpers import generar_token
from flask import send_file
from io import BytesIO
from datetime import datetime


admin_civil_bp = Blueprint(
    "admin_civil",
    __name__,
    url_prefix="/admin/civil"
)


def obtener_boda_civil():
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

    # Número de registros realizados.
    total_invitados = len(
        todos_los_invitados
    )

    # Total de personas registradas.
    # Incluye al invitado principal y
    # todos sus acompañantes.
    total_personas = sum(
        invitado.pases or 0
        for invitado in todos_los_invitados
    )

    # Como el nuevo registro confirma
    # automáticamente la asistencia,
    # todos los registros con respuesta "si"
    # cuentan como confirmados.
    personas_confirmadas = sum(
        invitado.asistentes_confirmados or 0
        for invitado in todos_los_invitados
        if invitado.respuesta == "si"
    )

    # Porcentaje de personas confirmadas.
    porcentaje = 0

    if total_personas > 0:
        porcentaje = round(
            (
                personas_confirmadas
                / total_personas
            ) * 100
        )

    return render_template(
        "admin/civil/dashboard.html",
        boda=boda_civil,
        invitados=invitados,
        total_invitados=total_invitados,
        total_personas=total_personas,
        personas_confirmadas=personas_confirmadas,
        porcentaje=porcentaje,
        busqueda=busqueda
    )

@admin_civil_bp.route("/exportar-excel")
@login_requerido
def exportar_excel():

    invitados = (
        InvitadoCivil.query
        .order_by(InvitadoCivil.nombre)
        .all()
    )

    registros = []

    for invitado in invitados:

        acompanantes = []

        if invitado.acompanantes:
            acompanantes = (
                invitado.acompanantes
                .splitlines()
            )

        registros.append({
            "Invitado principal": invitado.nombre,
            "Teléfono": invitado.telefono or "",
            "Personas registradas": invitado.pases or 0,
            "Acompañante 1": (
                acompanantes[0]
                if len(acompanantes) > 0
                else ""
            ),
            "Acompañante 2": (
                acompanantes[1]
                if len(acompanantes) > 1
                else ""
            ),
            "Acompañante 3": (
                acompanantes[2]
                if len(acompanantes) > 2
                else ""
            ),
            "Acompañante 4": (
                acompanantes[3]
                if len(acompanantes) > 3
                else ""
            ),
            "Acompañante 5": (
                acompanantes[4]
                if len(acompanantes) > 4
                else ""
            ),
            "Estado": (
                "Confirmado"
                if invitado.respuesta == "si"
                else "Pendiente"
            ),
            "Asistentes confirmados": (
                invitado.asistentes_confirmados or 0
            ),
            "Comentarios": (
                invitado.comentarios or ""
            ),
            "Fecha de confirmación": (
                invitado.fecha_confirmacion or ""
            ),
            "Token": invitado.token
        })

    df = pd.DataFrame(registros)

    archivo = BytesIO()

    with pd.ExcelWriter(
        archivo,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Invitados"
        )

        hoja = writer.sheets["Invitados"]

        for columna in hoja.columns:

            longitud = 0

            for celda in columna:

                if celda.value is not None:
                    longitud = max(
                        longitud,
                        len(str(celda.value))
                    )

            hoja.column_dimensions[
                columna[0].column_letter
            ].width = min(
                longitud + 2,
                40
            )

        hoja.freeze_panes = "A2"
        hoja.auto_filter.ref = (
            hoja.dimensions
        )

    archivo.seek(0)

    nombre_archivo = (
        "invitados_boda_civil_"
        + datetime.now().strftime("%Y%m%d_%H%M")
        + ".xlsx"
    )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        )
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
                "La cantidad de personas debe "
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
                "La cantidad de personas debe "
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

        boda_civil.nombre_novia = (
            request.form.get(
                "nombre_novia",
                ""
            ).strip()
        )

        boda_civil.nombre_novio = (
            request.form.get(
                "nombre_novio",
                ""
            ).strip()
        )

        boda_civil.fecha = (
            request.form.get(
                "fecha",
                ""
            ).strip()
        )

        boda_civil.hora = (
            request.form.get(
                "hora",
                ""
            ).strip()
        )

        boda_civil.lugar = (
            request.form.get(
                "lugar",
                ""
            ).strip()
        )

        boda_civil.direccion = (
            request.form.get(
                "direccion",
                ""
            ).strip()
        )

        boda_civil.mapa_url = (
            request.form.get(
                "mapa_url",
                ""
            ).strip()
        )

        boda_civil.mensaje_bienvenida = (
            request.form.get(
                "mensaje_bienvenida",
                ""
            ).strip()
        )

        boda_civil.mesa_regalos = (
            request.form.get(
                "mesa_regalos",
                ""
            ).strip()
        )

        boda_civil.mensaje_mesa_regalos = (
            request.form.get(
                "mensaje_mesa_regalos",
                ""
            ).strip()
        )

        boda_civil.imagen_1 = (
            request.form.get(
                "imagen_1",
                ""
            ).strip()
        )

        boda_civil.imagen_2 = (
            request.form.get(
                "imagen_2",
                ""
            ).strip()
        )

        boda_civil.imagen_3 = (
            request.form.get(
                "imagen_3",
                ""
            ).strip()
        )

        boda_civil.imagen_4 = (
            request.form.get(
                "imagen_4",
                ""
            ).strip()
        )

        boda_civil.imagen_5 = (
            request.form.get(
                "imagen_5",
                ""
            ).strip()
        )

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