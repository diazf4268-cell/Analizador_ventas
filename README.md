Analizador de Ventas con IA

Aplicación inteligente basada en modelos de lenguaje locales (LLMs) para análisis de KPIs, detección de anomalías y chat inteligente sobre datasets CSV.


#  Tecnologías Utilizadas

- Python
- Streamlit
- Ollama
- LangChain
- FAISS
- HuggingFace Embeddings
- Plotly
- DeepEval
- Opik


#  Funcionalidades

##  Dashboard Inteligente

- KPIs automáticos
- métricas de ventas
- gráficas interactivas
- análisis visual


## Agentes IA

### KPI Agent
Analiza indicadores clave de negocio.

### Anomaly Agent
Detecta anomalías en ventas.

### RAG Agent
Responde preguntas usando búsqueda semántica.


##  Pipeline RAG

El sistema implementa:

- chunking
- embeddings
- vector store
- búsqueda semántica
- retrieval augmented generation


##  Chat Inteligente

Permite hacer preguntas sobre datasets CSV usando LLMs locales.


##  Observabilidad

Integración con:

- Opik
- DeepEval

para monitoreo y evaluación de modelos.


#  Modelos Utilizados

Modelos locales ejecutados con Ollama:

- phi3
- tinyllama
- mistral

---

#  Estructura del Proyecto

```bash
agents/
data/
evaluacion/
rag/
utils/
Aplicacion.py
requirements.txt
README.md