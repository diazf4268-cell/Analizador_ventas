from langchain_ollama import ChatOllama
from agents.memoria import historial_conversacion

llm = ChatOllama(model="tinyllama")

# =========================
# REPORTE IA
# =========================

def generar_reporte(
    ventas_totales,
    promedio,
    maximo,
    minimo
):

    prompt = f"""
    Analiza estos KPIs:

    Ventas totales: {ventas_totales}
    Promedio: {promedio}
    Máximo: {maximo}
    Mínimo: {minimo}

    Genera:
    - Insights
    - Posibles anomalías
    - Recomendaciones
    """

    respuesta = llm.invoke(prompt)

    return respuesta.content


# =========================
# CHAT IA
# =========================

def generar_chat(prompt):

    # UNIR HISTORIAL
    contexto_memoria = "\n".join(
        historial_conversacion
    )

    prompt_final = f"""
    Historial de conversación:

    {contexto_memoria}

    Nueva pregunta:

    {prompt}
    """

    respuesta = llm.invoke(prompt_final)

    # GUARDAR MEMORIA
    historial_conversacion.append(
        f"Usuario: {prompt}"
    )

    historial_conversacion.append(
        f"IA: {respuesta.content}"
    )

    return respuesta.content