# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from scipy.stats import norm, chi2, kstwo

def mean_test(numbers: list[float], alpha: float) -> tuple[tuple[float, float], float, bool]:
    """
    Realiza la prueba de medias para verificar si el valor esperado de la muestra
    es estadísticamente igual a 0.5.

    Parámetros:
        numbers (list[float]): Lista de números pseudoaleatorios en el intervalo [0, 1).
        alpha (float): Nivel de significación (ej. 0.05).

    Retorna:
        tuple: (límites (LI, LS), estadístico (media muestral), passed (bool))
    """
    n = len(numbers)
    if n <= 0:
        raise ValueError("El tamaño de la muestra debe ser mayor que 0.")
    if not (0 < alpha < 1):
        raise ValueError("El nivel de significancia alpha debe estar en el intervalo (0, 1).")

    sample_mean = float(np.mean(numbers))
    
    # Z_(alpha/2) para la distribución normal estándar
    z_critical = float(norm.ppf(1 - alpha / 2))
    
    precision = z_critical * (1.0 / (12 * n) ** 0.5)
    lower_limit = 0.5 - precision
    upper_limit = 0.5 + precision
    
    passed = bool(lower_limit <= sample_mean <= upper_limit)
    
    return (lower_limit, upper_limit), sample_mean, passed

def variance_test(numbers: list[float], alpha: float) -> tuple[tuple[float, float], float, bool]:
    """
    Realiza la prueba de varianza para verificar si la dispersión de la muestra
    es estadísticamente igual a 1/12 (~0.08333).

    Parámetros:
        numbers (list[float]): Lista de números pseudoaleatorios en el intervalo [0, 1).
        alpha (float): Nivel de significación (ej. 0.05).

    Retorna:
        tuple: (límites (LI, LS), estadístico (varianza muestral), passed (bool))
    """
    n = len(numbers)
    if n <= 1:
        raise ValueError("El tamaño de la muestra debe ser mayor que 1 para calcular la varianza.")
    if not (0 < alpha < 1):
        raise ValueError("El nivel de significancia alpha debe estar en el intervalo (0, 1).")

    sample_var = float(np.var(numbers, ddof=1))
    
    # Percentiles chi-cuadrado para n-1 grados de libertad
    df = n - 1
    chi_lower = float(chi2.ppf(alpha / 2, df=df))
    chi_upper = float(chi2.ppf(1 - alpha / 2, df=df))
    
    lower_limit = chi_lower / (12 * df)
    upper_limit = chi_upper / (12 * df)
    
    passed = bool(lower_limit <= sample_var <= upper_limit)
    
    return (lower_limit, upper_limit), sample_var, passed

def ks_test(numbers: list[float], alpha: float) -> tuple[tuple[float, float], float, bool]:
    """
    Realiza la prueba de bondad de ajuste de Kolmogorov-Smirnov (KS) para
    verificar si la muestra sigue una distribución uniforme U(0, 1).

    Parámetros:
        numbers (list[float]): Lista de números pseudoaleatorios en el intervalo [0, 1).
        alpha (float): Nivel de significación (ej. 0.05).

    Retorna:
        tuple: (límites (0.0, D_critical), estadístico D, passed (bool))
    """
    n = len(numbers)
    if n <= 0:
        raise ValueError("El tamaño de la muestra debe ser mayor que 0.")
    if not (0 < alpha < 1):
        raise ValueError("El nivel de significancia alpha debe estar en el intervalo (0, 1).")

    sorted_numbers = np.sort(numbers)
    i = np.arange(1, n + 1)
    
    d_plus = np.max(i / n - sorted_numbers)
    d_minus = np.max(sorted_numbers - (i - 1) / n)
    d_statistic = float(max(d_plus, d_minus))
    
    # Valor crítico usando la distribución kstwo
    d_critical = float(kstwo.ppf(1 - alpha, n))
    
    passed = bool(d_statistic < d_critical)
    
    return (0.0, d_critical), d_statistic, passed
