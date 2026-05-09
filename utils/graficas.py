import plotly.express as px
import pandas as pd

def crear_grafica(df):

    posibles_fechas = [
        "fecha",
        "date",
        "orderdate",
        "datetime",
        "time"
    ]

    columna_fecha = None

    # BUSCAR COLUMNA FECHA
    for col in df.columns:

        if col.lower().strip() in posibles_fechas:

            columna_fecha = col

            break

    # SI EXISTE FECHA
    if columna_fecha is not None:

        # CONVERTIR A DATETIME
        df[columna_fecha] = pd.to_datetime(
            df[columna_fecha],
            errors="coerce"
        )

        fig = px.line(
            df,
            x=columna_fecha,
            y="ventas",
            title="Ventas en el tiempo"
        )

    else:

        # GRÁFICA SIMPLE
        fig = px.line(
            df,
            y="ventas",
            title="Ventas"
        )

    return fig