# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import List, Optional


class TestResult(BaseModel):
    """Estadísticas y límites de aceptación para una prueba estadística."""
    lower_limit: float = Field(..., description="Límite inferior de aceptación")
    upper_limit: float = Field(..., description="Límite superior de aceptación")
    statistic: float = Field(..., description="Valor del estadístico de prueba calculado")
    passed: bool = Field(..., description="Indica si la secuencia pasa la prueba estadística")


class SimulationRequest(BaseModel):
    """Esquema de entrada para solicitar la generación y validación de números pseudoaleatorios."""
    method: str = Field(
        ...,
        description="Método de generación: 'lcg' (Lineal), 'mcg' (Multiplicativo) o 'mid_square' (Cuadrados Medios)"
    )
    semilla: int = Field(
        ...,
        gt=0,
        description="Valor inicial de la semilla (debe ser estrictamente positivo)"
    )
    a: Optional[int] = Field(
        None,
        description="Constante multiplicadora (requerido para lcg y mcg)"
    )
    c: Optional[int] = Field(
        None,
        description="Constante de incremento (requerido para lcg)"
    )
    m: Optional[int] = Field(
        None,
        gt=0,
        description="Constante del módulo (requerido para lcg y mcg, debe ser estrictamente positivo)"
    )
    n: int = Field(
        ...,
        ge=0,
        description="Cantidad de números pseudoaleatorios a generar (entero no negativo)"
    )
    digits: Optional[int] = Field(
        None,
        description="Cantidad de dígitos a usar en Mid-Square (debe ser un entero positivo par)"
    )
    alpha: float = Field(
        ...,
        gt=0.0,
        lt=1.0,
        description="Nivel de significación para las pruebas estadísticas (estrictamente entre 0 y 1)"
    )


class SimulationResponse(BaseModel):
    """Esquema de salida con la secuencia generada y el resultado de las tres pruebas estadísticas."""
    numbers: List[float] = Field(
        ...,
        description="Lista de números pseudoaleatorios normalizados generados en el rango [0, 1)"
    )
    mean_test: TestResult = Field(
        ...,
        description="Resultado detallado de la prueba estadística de medias"
    )
    variance_test: TestResult = Field(
        ...,
        description="Resultado detallado de la prueba estadística de varianzas"
    )
    ks_test: TestResult = Field(
        ...,
        description="Resultado detallado de la prueba de bondad de ajuste Kolmogorov-Smirnov (KS)"
    )
