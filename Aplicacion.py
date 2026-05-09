# =========================================================
# IMPORTACIONES
# =========================================================

import csv
from io import StringIO

import pandas as pd
import streamlit as st

# =========================================================
# IMPORTACIONES LOCALES
# =========================================================

from utils.analisis import calcular_kpis
from utils.graficas import crear_grafica
from utils.anomalias import detectar_anomalias

from rag.vectorstore import crear_vectorstore
from rag.rag_agent import preguntar_rag

from agents.anomaly_agent import explicar_anomalias
from agents.agente_ia import generar_reporte, generar_chat
from evaluacion.opik_logger import guardar_log


# =========================================================
# CONFIGURACIÓN STREAMLIT
# =========================================================

st.set_page_config(
    page_title="Agente IA KPIs",
    layout="wide"
)

st.title("📊 Agente IA de KPIs")


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def leer_csv_seguro(archivo):
    """
    Lee un CSV detectando:
    - Codificación
    - Separador
    """

    contenido = archivo.read()

    encodings = [
        "utf-8",
        "latin1",
        "cp1252",
        "ISO-8859-1"
    ]

    texto = None

    # -----------------------------------------------------
    # DETECTAR CODIFICACIÓN
    # -----------------------------------------------------

    for enc in encodings:

        try:
            texto = contenido.decode(enc)
            break

        except:
            continue

    if texto is None:
        raise Exception(
            "No se pudo leer el archivo CSV"
        )

    # -----------------------------------------------------
    # DETECTAR SEPARADOR
    # -----------------------------------------------------

    muestra = texto[:2048]

    separador = csv.Sniffer().sniff(
        muestra,
        delimiters=";,|\t,"
    ).delimiter

    # -----------------------------------------------------
    # LEER DATAFRAME
    # -----------------------------------------------------

    df = pd.read_csv(
        StringIO(texto),
        sep=separador,
        engine="python",
        on_bad_lines="skip"
    )

    return df, separador


def limpiar_columnas(df):
    """
    Limpia nombres de columnas
    """

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
    )

    return df


def detectar_columna_ventas(df):
    """
    Detecta automáticamente la columna de ventas
    """

    posibles_ventas = [
        "ventas",
        "venta",
        "sales",
        "monto",
        "total",
        "valor",
        "revenue",
        "income",
        "ganancias",
        "facturacion",
        "importe",
        "amount",
        "precio",
        "price"
    ]

    # -----------------------------------------------------
    # BUSCAR POR NOMBRE
    # -----------------------------------------------------

    for col in df.columns:

        if col.lower().strip() in posibles_ventas:
            return col

    # -----------------------------------------------------
    # BUSCAR COLUMNAS NUMÉRICAS
    # -----------------------------------------------------

    columnas_numericas = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if columnas_numericas:
        return columnas_numericas[0]

    return None


def preparar_dataframe(df):
    """
    Limpia y prepara el dataframe
    """

    df = limpiar_columnas(df)

    columna_ventas = detectar_columna_ventas(df)

    if columna_ventas is None:
        raise Exception(
            "No se encontró una columna numérica de ventas"
        )

    # -----------------------------------------------------
    # RENOMBRAR COLUMNA
    # -----------------------------------------------------

    df.rename(
        columns={
            columna_ventas: "ventas"
        },
        inplace=True
    )

    # -----------------------------------------------------
    # CONVERTIR A NUMÉRICO
    # -----------------------------------------------------

    df["ventas"] = pd.to_numeric(
        df["ventas"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # ELIMINAR NULOS
    # -----------------------------------------------------

    df = df.dropna(subset=["ventas"])

    if df.empty:
        raise Exception(
            "No quedaron datos válidos"
        )

    return df


# =========================================================
# SECCIÓN RAG
# =========================================================

st.subheader("📚 RAG - Documentos")

archivo_txt = st.file_uploader(
    "Sube un archivo TXT",
    type=["txt"]
)

if archivo_txt is not None:

    texto = archivo_txt.read().decode()

    vectorstore = crear_vectorstore(texto)

    st.success(
        "✅ VectorStore creado correctamente"
    )

    pregunta_rag = st.text_input(
        "Pregunta sobre el documento"
    )

    if pregunta_rag:

        respuesta_rag = preguntar_rag(
            vectorstore,
            pregunta_rag
        )

        st.write(respuesta_rag)


# =========================================================
# SUBIR CSV
# =========================================================

archivo = st.file_uploader(
    "📁 Sube un archivo CSV",
    type=["csv"]
)


# =========================================================
# PROCESAMIENTO PRINCIPAL
# =========================================================

if archivo is not None:

    try:

        # -------------------------------------------------
        # LEER CSV
        # -------------------------------------------------

        df, separador = leer_csv_seguro(
            archivo
        )

        # -------------------------------------------------
        # PREPARAR DATAFRAME
        # -------------------------------------------------

        df = preparar_dataframe(df)

        # -------------------------------------------------
        # MOSTRAR INFORMACIÓN
        # -------------------------------------------------

        st.success(
            f"✅ CSV cargado correctamente | "
            f"Separador detectado: '{separador}'"
        )

        st.subheader("📌 Columnas Detectadas")

        st.write(df.columns.tolist())

        st.subheader("📁 Datos")

        st.dataframe(df)

        # =================================================
        # KPIs
        # =================================================

        ventas_totales, promedio, maximo, minimo = (
            calcular_kpis(df)
        )

        st.subheader("📊 KPIs")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Total",
            round(ventas_totales, 2)
        )

        col2.metric(
            "📈 Promedio",
            round(promedio, 2)
        )

        col3.metric(
            "🔥 Máximo",
            round(maximo, 2)
        )

        col4.metric(
            "📉 Mínimo",
            round(minimo, 2)
        )

        # =================================================
        # GRÁFICA
        # =================================================

        st.subheader("📊 Gráfica")

        fig = crear_grafica(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =================================================
        # ANOMALÍAS
        # =================================================

        st.subheader("🚨 Anomalías Detectadas")

        anomalias = detectar_anomalias(df)

        st.dataframe(anomalias)

        # -------------------------------------------------
        # EXPLICAR ANOMALÍAS
        # -------------------------------------------------

        if st.button("🧠 Explicar anomalías"):

            with st.spinner(
                "Analizando anomalías..."
            ):

                explicacion = explicar_anomalias(
                    anomalias
                )

            st.subheader(
                "📌 Explicación IA"
            )

            st.write(explicacion)

        # =================================================
        # REPORTE IA
        # =================================================

        st.subheader("🤖 Reporte IA")

        if st.button("Generar Reporte IA"):

            with st.spinner(
                "Generando reporte..."
            ):

                reporte = generar_reporte(
                    ventas_totales,
                    promedio,
                    maximo,
                    minimo
                )

            st.write(reporte)

        # =================================================
        # CHAT IA
        # =================================================

        st.subheader("💬 Chat Inteligente")

        pregunta = st.text_input(
            "Haz una pregunta sobre tus datos"
        )

        if pregunta:

            contexto = df.head(20).to_string()

            prompt_chat = f"""
Eres un analista de datos.

IMPORTANTE:
- Responde SOLO usando el dataset.
- NO inventes información.
- Si no encuentras la respuesta,
  dilo claramente.
- NO hables de otros temas.

DATASET:

{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""

            with st.spinner(
                "Analizando datos..."
            ):

                respuesta_chat = generar_chat(
                    prompt_chat
                )

            st.subheader("🤖 Respuesta IA")

            st.write(respuesta_chat)
            guardar_log(
                pregunta,
                respuesta_chat
            )

    except Exception as e:

        st.error(
            f"❌ Error leyendo CSV: {e}"
        )