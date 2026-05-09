from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="tinyllama"
)

def preguntar_rag(
    vectorstore,
    pregunta
):

    # BÚSQUEDA SEMÁNTICA
    docs = vectorstore.similarity_search(
        pregunta,
        k=3
    )

    # UNIR CONTEXTO
    contexto = "\n".join([
        doc.page_content
        for doc in docs
    ])

    # PROMPT
    prompt = f"""
    Responde usando SOLO este contexto:

    {contexto}

    Pregunta:
    {pregunta}
    """

    respuesta = llm.invoke(prompt)

    return respuesta.content