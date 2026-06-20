import secrets
import random
import string



def generar_token():

    caracteres = (
        string.ascii_uppercase +
        string.digits
    )

    return "".join(
        random.choice(caracteres)
        for _ in range(6)
    )