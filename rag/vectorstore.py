from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

from rag.embeddings import embeddings

def crear_vectorstore(texto):

    # DIVIDIR TEXTO
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(texto)

    # CREAR VECTOR DB
    vectorstore = FAISS.from_texts(
        chunks,
        embeddings
    )

    return vectorstore