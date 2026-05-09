from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="tinyllama"
)

def explicar_anomalias(anomalias):

    contexto = anomalias.to_string()

    prompt = f"""
    Eres un experto en detección
    de anomalías empresariales.

    Estas anomalías fueron detectadas:

    {contexto}

    Explica:
    - posibles causas
    - riesgos
    - recomendaciones
    """

    respuesta = llm.invoke(prompt)

    return respuesta.content