from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="tinyllama"
)

def analizar_kpis(
    ventas_totales,
    promedio,
    maximo,
    minimo
):

    prompt = f"""
    Eres un analista financiero experto.

    Analiza estos KPIs:

    Ventas Totales: {ventas_totales}
    Promedio: {promedio}
    Máximo: {maximo}
    Mínimo: {minimo}

    Genera:
    - análisis ejecutivo
    - riesgos
    - recomendaciones
    """

    respuesta = llm.invoke(prompt)

    return respuesta.content