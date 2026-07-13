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

def runs_test(numbers: list[float], alpha: float) -> tuple[tuple[float, float], float, bool]:
    """
    Realiza la prueba de rachas arriba y abajo de la media para verificar la independencia
    de la muestra de números pseudoaleatorios en el intervalo [0, 1).

    Parámetros:
        numbers (list[float]): Lista de números pseudoaleatorios en el intervalo [0, 1).
        alpha (float): Nivel de significación (ej. 0.05).

    Retorna:
        tuple: (límites (LI, LS), estadístico Z_0, passed (bool))
    """
    n = len(numbers)
    if n <= 1:
        raise ValueError("El tamaño de la muestra debe ser mayor que 1 para la prueba de rachas.")
    if not (0 < alpha < 1):
        raise ValueError("El nivel de significancia alpha debe estar en el intervalo (0, 1).")

    # Clasificar respecto a la media teórica (0.5)
    # n1: cantidad >= 0.5
    # n2: cantidad < 0.5
    signs = [1 if x >= 0.5 else 0 for x in numbers]
    n1 = sum(signs)
    n2 = n - n1

    # Contar corridas/rachas
    runs = 1
    for i in range(1, n):
        if signs[i] != signs[i - 1]:
            runs += 1

    # Si todo cae en un lado, no pasa la prueba (no es independiente)
    if n1 == 0 or n2 == 0:
        z_critical = float(norm.ppf(1 - alpha / 2))
        return (-z_critical, z_critical), float('inf'), False

    # Media esperada de rachas
    mu_runs = (2 * n1 * n2) / n + 1.0
    
    # Varianza de rachas
    var_numerator = 2 * n1 * n2 * (2 * n1 * n2 - n)
    var_denominator = (n ** 2) * (n - 1)
    
    if var_denominator == 0 or var_numerator <= 0:
        z_statistic = 0.0
    else:
        sigma_runs = (var_numerator / var_denominator) ** 0.5
        z_statistic = (runs - mu_runs) / sigma_runs

    z_critical = float(norm.ppf(1 - alpha / 2))
    lower_limit = -z_critical
    upper_limit = z_critical

    passed = bool(lower_limit <= z_statistic <= upper_limit)
    return (lower_limit, upper_limit), float(z_statistic), passed

