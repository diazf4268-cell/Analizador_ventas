from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

# RESPUESTA GENERADA
respuesta = """
Las ventas muestran un comportamiento positivo.
El promedio indica estabilidad.
"""

# TEST CASE
test_case = LLMTestCase(
    input="Analiza los KPIs",
    actual_output=respuesta
)

# MÉTRICA
metric = AnswerRelevancyMetric(
    threshold=0.5
)

# EVALUAR
metric.measure(test_case)

print("\nScore:", metric.score)

print("\nReason:", metric.reason)