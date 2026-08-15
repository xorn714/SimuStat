# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class TestResult(BaseModel):
    """Estadísticas y límites de aceptación para una prueba estadística."""
    lower_limit: float = Field(..., description="Límite inferior de aceptación")
    upper_limit: float = Field(..., description="Límite superior de aceptación")
    statistic: float = Field(..., description="Valor del estadístico de prueba calculado")
    passed: bool = Field(..., description="Indica si la secuencia pasa la prueba estadística")


class DistributionTestResult(BaseModel):
    """Resultado de las cuatro pruebas estadísticas aplicadas a la variable aleatoria transformada."""
    mean_test: Optional[TestResult] = Field(None, description="Prueba de medias de la variable transformada")
    variance_test: Optional[TestResult] = Field(None, description="Prueba de varianza de la variable transformada")
    ks_test: Optional[TestResult] = Field(None, description="Prueba KS de la variable transformada")
    streak_test: Optional[TestResult] = Field(None, description="Prueba de rachas de la variable transformada")


class DiscreteStatsResponse(BaseModel):
    """Estadísticos empíricos vs teóricos para una distribución discreta."""
    sample_size: int = Field(..., description="Cantidad de valores generados")
    empirical_mean: float = Field(..., description="Media muestral empírica")
    empirical_variance: float = Field(..., description="Varianza muestral empírica")
    theoretical_mean: float = Field(..., description="Media teórica de la distribución")
    theoretical_variance: float = Field(..., description="Varianza teórica de la distribución")
    mean_diff: float = Field(..., description="Diferencia absoluta entre media empírica y teórica")
    variance_diff: float = Field(..., description="Diferencia absoluta entre varianza empírica y teórica")
    frequencies: Dict[int, int] = Field(..., description="Frecuencia absoluta por valor")
    relative_frequencies: Dict[int, float] = Field(..., description="Frecuencia relativa por valor")
    unique_values: int = Field(..., description="Cantidad de valores distintos")
    min_value: int = Field(..., description="Valor mínimo observado")
    max_value: int = Field(..., description="Valor máximo observado")
    mode: Optional[int] = Field(None, description="Valor con mayor frecuencia (moda)")


class DiscreteHistogramPoint(BaseModel):
    """Punto de un histograma de barras para una distribución discreta."""
    value: int = Field(..., description="Valor entero de la barra")
    count: int = Field(..., description="Frecuencia absoluta")
    relative_frequency: float = Field(..., description="Frecuencia relativa")
    cumulative_count: int = Field(..., description="Frecuencia absoluta acumulada")
    cumulative_relative: float = Field(..., description="Frecuencia relativa acumulada")


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
    distribution_type: Optional[str] = Field(
        None,
        description="Tipo de variable a transformar: 'continuous', 'discrete' o 'none'"
    )
    distribution_name: Optional[str] = Field(
        None,
        description="Nombre de la distribución: continuas ('uniform', 'exponential', 'normal', 'weibull') "
                    "o discretas ('bernoulli', 'binomial', 'poisson', 'geometric', 'negative_binomial', 'hypergeometric', 'uniform_discrete')"
    )
    continuous_dist: Optional[str] = Field(
        None,
        description="Distribución continua (compatibilidad): 'uniform', 'exponential', 'normal', 'weibull' o 'none'"
    )
    discrete_dist: Optional[str] = Field(
        None,
        description="Distribución discreta (compatibilidad): 'bernoulli', 'binomial', 'poisson', "
                    "'geometric', 'negative_binomial', 'hypergeometric', 'uniform_discrete'"
    )
    dist_params: Optional[dict] = Field(
        None,
        description="Parámetros de la distribución elegida (ej. a, b, lambd, mean, std_dev, alpha, beta, p, n, r, N, K, i, j)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "method": "lcg",
                    "semilla": 37,
                    "a": 19,
                    "c": 33,
                    "m": 100,
                    "n": 50,
                    "digits": 0,
                    "alpha": 0.05,
                    "distribution_type": "continuous",
                    "distribution_name": "uniform",
                    "dist_params": {"a": 0.0, "b": 1.0},
                },
                {
                    "method": "mcg",
                    "semilla": 17,
                    "a": 3,
                    "m": 100,
                    "n": 100,
                    "alpha": 0.05,
                    "distribution_type": "discrete",
                    "distribution_name": "binomial",
                    "dist_params": {"n": 10, "p": 0.5},
                },
            ]
        }
    }


class SimulationResponse(BaseModel):
    """Esquema de salida con la secuencia generada y el resultado de las pruebas estadísticas."""
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
    streak_test: TestResult = Field(
        ...,
        description="Resultado detallado de la prueba de rachas (streak/runs test) arriba y abajo de la media"
    )
    distribution_tests: Optional[DistributionTestResult] = Field(
        None,
        description="Resultado de las cuatro pruebas estadísticas aplicadas a la variable transformada (continua o discreta)"
    )
    continuous_values: Optional[List[float]] = Field(
        None,
        description="Valores de la variable aleatoria continua generada si fue solicitada"
    )
    continuous_stats: Optional[dict] = Field(
        None,
        description="Estadísticos empíricos y teóricos de la variable aleatoria continua"
    )
    histogram: Optional[dict] = Field(
        None,
        description="Datos de bins e histograma de frecuencias con curva de densidad teórica"
    )
    discrete_values: Optional[List[int]] = Field(
        None,
        description="Valores de la variable aleatoria discreta generada si fue solicitada"
    )
    discrete_stats: Optional[DiscreteStatsResponse] = Field(
        None,
        description="Estadísticos empíricos y teóricos de la variable aleatoria discreta"
    )
    discrete_histogram: Optional[List[DiscreteHistogramPoint]] = Field(
        None,
        description="Datos de barras del histograma de la variable aleatoria discreta"
    )
