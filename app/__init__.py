from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    from app.models.boda import Boda
    from app.models.invitado import Invitado
    from app.models.administrador import Administrador
    from app.models.mesa import Mesa

    from app.routes.public import public_bp
    from app.routes.admin import admin_bp
    from app.routes.invitados import invitados_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(invitados_bp)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def pagina_no_encontrada(error):

        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def error_servidor(error):

        return render_template("errors/500.html"), 500

    return app