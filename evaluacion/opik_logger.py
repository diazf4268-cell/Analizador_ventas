from datetime import datetime

def guardar_log(
    pregunta,
    respuesta
):

    with open(
        "reports/logs.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"""
Fecha: {datetime.now()}

Pregunta:
{pregunta}

Respuesta:
{respuesta}

--------------------------------
"""
        )