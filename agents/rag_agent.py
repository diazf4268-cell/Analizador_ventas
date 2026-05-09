from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="tinyllama"
)

def responder_documento(
    contexto,
    pregunta
):

    prompt = f"""
    Responde usando SOLO
    el siguiente contexto:

    {contexto}

    Pregunta:
    {pregunta}
    """

    respuesta = llm.invoke(prompt)

    return respuesta.content