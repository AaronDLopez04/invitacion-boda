from functools import wraps

from flask import session
from flask import redirect
from flask import url_for


def login_requerido(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get(
            "admin_logueado"
        ):

            return redirect(
                url_for(
                    "admin.login"
                )
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper