import io
import pandas as pd

from flask import send_file


class ExcelService:

    @staticmethod
    def exportar_invitados(invitados):

        datos = []

        for invitado in invitados:

            datos.append({
                "Nombre": invitado.nombre,
                "Teléfono": invitado.telefono,
                "Pases": invitado.pases,
                "Token": invitado.token,
                "Respuesta": invitado.respuesta,
                "Asistentes confirmados": invitado.asistentes_confirmados,
                "Comentarios": invitado.comentarios,
                "Fecha confirmación": invitado.fecha_confirmacion
            })

        return ExcelService._crear_excel(
            datos,
            "invitados.xlsx"
        )

    @staticmethod
    def exportar_confirmaciones(invitados):

        datos = []

        for invitado in invitados:

            datos.append({
                "Nombre": invitado.nombre,
                "Respuesta": invitado.respuesta,
                "Pases": invitado.pases,
                "Asistentes confirmados": invitado.asistentes_confirmados,
                "Comentarios": invitado.comentarios,
                "Fecha confirmación": invitado.fecha_confirmacion
            })

        return ExcelService._crear_excel(
            datos,
            "confirmaciones.xlsx"
        )

    @staticmethod
    def exportar_estadisticas(
        total_invitados,
        total_pases,
        asistentes_confirmados,
        no_asistiran,
        pendientes
    ):

        datos = [
            {
                "Concepto": "Invitados registrados",
                "Cantidad": total_invitados
            },
            {
                "Concepto": "Pases otorgados",
                "Cantidad": total_pases
            },
            {
                "Concepto": "Asistentes confirmados",
                "Cantidad": asistentes_confirmados
            },
            {
                "Concepto": "Personas que no asistirán",
                "Cantidad": no_asistiran
            },
            {
                "Concepto": "Invitaciones pendientes",
                "Cantidad": pendientes
            }
        ]

        return ExcelService._crear_excel(
            datos,
            "estadisticas.xlsx"
        )

    @staticmethod
    def _crear_excel(datos, nombre_archivo):

        output = io.BytesIO()

        df = pd.DataFrame(datos)

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Reporte"
            )

        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    @staticmethod
    def exportar_mesas(mesas):

        datos = []

        for mesa in mesas:

            if mesa.invitados:

                for invitado in mesa.invitados:

                    datos.append({
                        "Mesa": mesa.nombre,
                        "Capacidad": mesa.capacidad,
                        "Invitado": invitado.nombre,
                        "Pases": invitado.pases,
                        "Respuesta": invitado.respuesta,
                        "Asistentes confirmados": invitado.asistentes_confirmados,
                        "Personas ingresadas": invitado.personas_ingresadas
                    })

            else:

                datos.append({
                    "Mesa": mesa.nombre,
                    "Capacidad": mesa.capacidad,
                    "Invitado": "Sin invitados",
                    "Pases": 0,
                    "Respuesta": "",
                    "Asistentes confirmados": 0,
                    "Personas ingresadas": 0
                })

            return ExcelService._crear_excel(
                datos,
                "mesas.xlsx"
            )
        
    @staticmethod
    def exportar_checkin(invitados):

            datos = []

            for invitado in invitados:

                ingresados = invitado.personas_ingresadas or 0

                faltan = invitado.pases - ingresados

                datos.append({
                    "Nombre": invitado.nombre,
                    "Pases": invitado.pases,
                    "Asistentes confirmados": invitado.asistentes_confirmados or 0,
                    "Personas ingresadas": ingresados,
                    "Faltan por ingresar": faltan,
                    "Check-in completo": "Sí" if invitado.checkin_completo else "No",
                    "Último ingreso": invitado.hora_ingreso or "",
                    "Mesa": invitado.mesa.nombre if invitado.mesa else "Sin mesa"
                })

            return ExcelService._crear_excel(
                datos,
                "checkin.xlsx"
            )
        