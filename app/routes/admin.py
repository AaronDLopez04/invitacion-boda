import os

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from app.models.boda import Boda
from flask import current_app
from werkzeug.utils import secure_filename
from app.models.mesa import Mesa
from datetime import datetime
from flask import jsonify

from werkzeug.security import generate_password_hash

from app.services.excel_service import ExcelService

from app import db

from app.models.invitado import Invitado

from app.utils.auth import (
    login_requerido
)

from werkzeug.security import (
    check_password_hash
)

from app.models.administrador import (
    Administrador
)

from app.utils.helpers import generar_token
from app.services.qr_service import generar_credencial_qr

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        usuario = request.form.get(
            "usuario"
        )

        password = request.form.get(
            "password"
        )

        admin = Administrador.query.filter_by(
            usuario=usuario
            ).first()

        if (
        admin
        and
        check_password_hash(
            admin.password,
            password
            )
        ):

            session[
                "admin_logueado"
            ] = True

            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )

        return render_template(
            "admin/login.html",
            error=True
        )

    return render_template(
        "admin/login.html",
        error=False
    )


@admin_bp.route(
    "/logout"
)
def logout():

    session.clear()

    return redirect(
        url_for(
            "admin.login"
        )
    )


@admin_bp.route("/")
@login_requerido
def dashboard():

    busqueda = request.args.get(
        "q",
        ""
    )

    query = Invitado.query

    if busqueda:

        query = query.filter(
            Invitado.nombre.contains(
                busqueda
            )
        )

    invitados = query.order_by(
        Invitado.nombre
    ).all()

    total_invitados = Invitado.query.count()

    total_pases = sum(
        invitado.pases
        for invitado in Invitado.query.all()
    )


    asistentes_confirmados = sum(
        invitado.asistentes_confirmados or 0
        for invitado in Invitado.query.all()
    )

    no_asistiran = sum(
        invitado.pases
        for invitado in Invitado.query.filter_by(
            respuesta="no"
        ).all()
    )

    pendientes = Invitado.query.filter_by(
        respuesta="pendiente"
    ).count()

    porcentaje = 0

    if total_pases > 0:

        porcentaje = round(
            (
                asistentes_confirmados /
                total_pases
            ) * 100
        )

    personas_ingresadas = sum(
    invitado.personas_ingresadas or 0
    for invitado in Invitado.query.all()
    )

    personas_por_llegar = total_pases - personas_ingresadas

    checkin_completos = Invitado.query.filter_by(
    checkin_completo=True
    ).count()

    return render_template(

        "admin/dashboard.html",

        invitados=invitados,

        total_invitados=total_invitados,

        total_pases=total_pases,

        asistentes_confirmados=asistentes_confirmados,

        no_asistiran=no_asistiran,

        pendientes=pendientes,

        porcentaje=porcentaje,

        busqueda=busqueda,

        personas_ingresadas=personas_ingresadas,

        personas_por_llegar=personas_por_llegar,

        checkin_completos=checkin_completos,
    )


@admin_bp.route(
    "/nuevo",
    methods=["GET", "POST"]
)
@login_requerido
def nuevo_invitado():

    if request.method == "POST":

        token = generar_token()

        while Invitado.query.filter_by(
            token=token
        ).first():

            token = generar_token()

        invitado = Invitado(

            nombre=request.form["nombre"],

            telefono=request.form["telefono"],

            pases=int(
                request.form["pases"]
            ),

            token=token

        )

        db.session.add(
            invitado
        )

        db.session.commit()

        boda = Boda.query.first()

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

        return redirect(
            url_for(
                "admin.dashboard"
            )
        )

    return render_template(
        "admin/nuevo_invitado.html"
    )


@admin_bp.route(
    "/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_requerido
def editar_invitado(id):

    invitado = Invitado.query.get_or_404(id)

    lista_mesas = Mesa.query.all()

    if request.method == "POST":

        invitado.nombre = request.form["nombre"]

        invitado.telefono = request.form["telefono"]

        invitado.pases = int(request.form["pases"])

        mesa_id = request.form.get("mesa_id")

        invitado.mesa_id = int(mesa_id) if mesa_id else None

        db.session.commit()

        return redirect(
            url_for("admin.dashboard")
        )

    return render_template(
        "admin/editar_invitado.html",
        invitado=invitado,
        mesas=lista_mesas
    )


@admin_bp.route(
    "/eliminar/<int:id>"
)
@login_requerido
def eliminar_invitado(id):

    invitado = Invitado.query.get_or_404(
        id
    )

    db.session.delete(
        invitado
    )

    db.session.commit()

    return redirect(
        url_for(
            "admin.dashboard"
        )
    )


@admin_bp.route(
    "/exportar"
)
@admin_bp.route("/exportar/invitados")
@login_requerido
def exportar_invitados():

    invitados = Invitado.query.order_by(
        Invitado.nombre
    ).all()

    return ExcelService.exportar_invitados(
        invitados
    )


@admin_bp.route("/exportar/confirmaciones")
@login_requerido
def exportar_confirmaciones():

    invitados = Invitado.query.order_by(
        Invitado.nombre
    ).all()

    return ExcelService.exportar_confirmaciones(
        invitados
    )


@admin_bp.route("/exportar/estadisticas")
@login_requerido
def exportar_estadisticas():

    invitados = Invitado.query.all()

    total_invitados = Invitado.query.count()

    total_pases = sum(
        invitado.pases
        for invitado in invitados
    )

    asistentes_confirmados = sum(
        invitado.asistentes_confirmados or 0
        for invitado in invitados
    )

    no_asistiran = sum(
        invitado.pases
        for invitado in Invitado.query.filter_by(
            respuesta="no"
        ).all()
    )

    pendientes = Invitado.query.filter_by(
        respuesta="pendiente"
    ).count()

    return ExcelService.exportar_estadisticas(
        total_invitados,
        total_pases,
        asistentes_confirmados,
        no_asistiran,
        pendientes
    )

@admin_bp.route(
    "/configuracion",
    methods=["GET", "POST"]
)
@login_requerido
def configuracion_boda():

    boda = Boda.query.first()

    if request.method == "POST":

        boda.nombre_novia = request.form["nombre_novia"]
        boda.nombre_novio = request.form["nombre_novio"]

        boda.fecha = request.form["fecha"]
        boda.hora = request.form["hora"]

        boda.versiculo = request.form["versiculo"]

        boda.mensaje_bienvenida = request.form["mensaje_bienvenida"]
        boda.historia = request.form["historia"]

        boda.lugar_ceremonia = request.form["lugar_ceremonia"]
        boda.direccion_ceremonia = request.form["direccion_ceremonia"]

        boda.codigo_vestimenta = request.form["codigo_vestimenta"]

        boda.mesa_regalos = request.form["mesa_regalos"]
        boda.hospedaje = request.form["hospedaje"]

        boda.whatsapp_novio = request.form["whatsapp_novio"]
        boda.whatsapp_novia = request.form["whatsapp_novia"]
        boda.whatsapp_hospedaje = request.form["whatsapp_hospedaje"]

        db.session.commit()

        return redirect(
            url_for("admin.configuracion_boda")
        )

    return render_template(
        "admin/configuracion_boda.html",
        boda=boda
    )

@admin_bp.route(
    "/multimedia",
    methods=["GET", "POST"]
)
@login_requerido
def multimedia():

    if request.method == "POST":

        archivos = {
            "portada": ("img", "portada.jpg"),
            "historia": ("img", "historia.jpg"),
            "pareja1": ("img", "pareja1.jpg"),
            "video": ("video", "pedida.mp4")
        }

        for campo, datos in archivos.items():

            carpeta, nombre_archivo = datos

            archivo = request.files.get(campo)

            if archivo and archivo.filename != "":

                ruta_carpeta = os.path.join(
                    current_app.root_path,
                    "static",
                    carpeta
                )

                os.makedirs(
                    ruta_carpeta,
                    exist_ok=True
                )

                ruta_final = os.path.join(
                    ruta_carpeta,
                    secure_filename(nombre_archivo)
                )

                archivo.save(ruta_final)

        return redirect(
            url_for("admin.multimedia")
        )

    return render_template(
        "admin/multimedia.html"
    )

@admin_bp.route(
    "/qr/<int:id>"
)
@login_requerido
def ver_qr(id):

    invitado = Invitado.query.get_or_404(
        id
    )

    boda = Boda.query.first()

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

    return render_template(
        "admin/ver_qr.html",
        invitado=invitado,
        boda=boda
    )

@admin_bp.route("/mesas", methods=["GET", "POST"])
@login_requerido
def mesas():

    if request.method == "POST":

        mesa = Mesa(
            nombre=request.form["nombre"],
            capacidad=int(request.form["capacidad"])
        )

        db.session.add(mesa)
        db.session.commit()

        return redirect(url_for("admin.mesas"))

    mesas = Mesa.query.order_by(Mesa.nombre).all()

    invitados_sin_mesa = Invitado.query.filter(
        Invitado.mesa_id.is_(None)
    ).order_by(
        Invitado.nombre
    ).all()

    return render_template(
        "admin/mesas.html",
        mesas=mesas,
        invitados_sin_mesa=invitados_sin_mesa
    )


@admin_bp.route("/mesas/asignar", methods=["POST"])
@login_requerido
def asignar_mesa():

    invitado_id = request.form.get("invitado_id")
    mesa_id = request.form.get("mesa_id")

    invitado = Invitado.query.get_or_404(invitado_id)

    invitado.mesa_id = int(mesa_id)

    db.session.commit()

    return redirect(url_for("admin.mesas"))


@admin_bp.route("/mesas/quitar/<int:invitado_id>")
@login_requerido
def quitar_mesa(invitado_id):

    invitado = Invitado.query.get_or_404(invitado_id)

    invitado.mesa_id = None

    db.session.commit()

    return redirect(url_for("admin.mesas"))


@admin_bp.route("/mesas/eliminar/<int:id>")
@login_requerido
def eliminar_mesa(id):

    mesa = Mesa.query.get_or_404(id)

    for invitado in mesa.invitados:
        invitado.mesa_id = None

    db.session.delete(mesa)
    db.session.commit()

    return redirect(url_for("admin.mesas"))


@admin_bp.route(
    "/checkin",
    methods=["GET", "POST"]
)
@login_requerido
def checkin():

    invitado = None
    error = None

    if request.method == "POST":

        token = request.form.get("token")

        invitado = Invitado.query.filter_by(
            token=token
        ).first()

        if not invitado:
            error = "Invitación no encontrada."

    return render_template(
        "admin/checkin.html",
        invitado=invitado,
        error=error
    )


@admin_bp.route(
    "/checkin/registrar/<int:id>",
    methods=["POST"]
)
@login_requerido
def registrar_checkin(id):

    invitado = Invitado.query.get_or_404(
        id
    )

    cantidad = int(
        request.form.get(
            "cantidad",
            0
        )
    )

    if cantidad < 0:

        cantidad = 0

    disponibles = invitado.pases - (
        invitado.personas_ingresadas or 0
    )

    if cantidad > disponibles:

        cantidad = disponibles

    invitado.personas_ingresadas = (
        invitado.personas_ingresadas or 0
    ) + cantidad

    if invitado.personas_ingresadas >= invitado.pases:

        invitado.checkin_completo = True

    else:

        invitado.checkin_completo = False

    invitado.hora_ingreso = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    db.session.commit()

    return redirect(
        url_for(
            "admin.checkin"
        )
    )

@admin_bp.route(
    "/mesas/asignar-rapido",
    methods=["POST"]
)
@login_requerido
def asignar_mesa_rapido():

    datos = request.get_json()

    invitado_id = datos.get("invitado_id")
    mesa_id = datos.get("mesa_id")

    invitado = Invitado.query.get_or_404(
        invitado_id
    )

    if mesa_id == "sin-mesa":

        invitado.mesa_id = None

    else:

        invitado.mesa_id = int(
            mesa_id
        )

    db.session.commit()

    return jsonify({
        "ok": True
    })

@admin_bp.route("/exportar/mesas")
@login_requerido
def exportar_mesas():

    mesas = Mesa.query.order_by(
        Mesa.nombre
    ).all()

    return ExcelService.exportar_mesas(
        mesas
    )
@admin_bp.route("/plano")
@login_requerido

def plano():

    mesas = Mesa.query.order_by(
        Mesa.nombre
    ).all()

    return render_template(
        "admin/plano.html",
        mesas=mesas
    )
@admin_bp.route(
    "/plano/guardar-posicion",
    methods=["POST"]
)
@login_requerido
def guardar_posicion_mesa():

    datos = request.get_json()

    mesa_id = datos.get("mesa_id")
    pos_x = int(datos.get("pos_x", 0))
    pos_y = int(datos.get("pos_y", 0))

    mesa = Mesa.query.get_or_404(
        mesa_id
    )

    mesa.pos_x = pos_x
    mesa.pos_y = pos_y

    db.session.commit()

    return jsonify({
        "ok": True
    })

@admin_bp.route("/reporte-recepcion")
@login_requerido
def reporte_recepcion():

    mesas = Mesa.query.order_by(
        Mesa.nombre
    ).all()

    invitados_sin_mesa = Invitado.query.filter(
        Invitado.mesa_id.is_(None)
    ).order_by(
        Invitado.nombre
    ).all()

    boda = Boda.query.first()

    return render_template(
        "admin/reporte_recepcion.html",
        mesas=mesas,
        invitados_sin_mesa=invitados_sin_mesa,
        boda=boda
    )

@admin_bp.route("/exportar/checkin")
@login_requerido
def exportar_checkin():

    invitados = Invitado.query.order_by(
        Invitado.nombre
    ).all()

    return ExcelService.exportar_checkin(
        invitados
    )

@admin_bp.route(
    "/mi-cuenta",
    methods=["GET", "POST"]
)
@login_requerido
def mi_cuenta():

    admin = Administrador.query.first()

    mensaje = None
    error = None

    if request.method == "POST":

        usuario = request.form.get("usuario")
        password_actual = request.form.get("password_actual")
        password_nuevo = request.form.get("password_nuevo")
        password_confirmar = request.form.get("password_confirmar")

        if usuario:
            admin.usuario = usuario

        if password_actual or password_nuevo or password_confirmar:

            if not check_password_hash(
                admin.password,
                password_actual
            ):

                error = "La contraseña actual no es correcta."

            elif password_nuevo != password_confirmar:

                error = "La nueva contraseña no coincide."

            elif len(password_nuevo) < 6:

                error = "La nueva contraseña debe tener al menos 6 caracteres."

            else:

                admin.password = generate_password_hash(
                    password_nuevo
                )

        if not error:

            db.session.commit()
            mensaje = "Cuenta actualizada correctamente."

    return render_template(
        "admin/mi_cuenta.html",
        admin=admin,
        mensaje=mensaje,
        error=error
    )