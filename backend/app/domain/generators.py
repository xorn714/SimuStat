# pyrefly: ignore
class GeneratorValidationError(ValueError):
    """Excepción lanzada cuando los parámetros de entrada de los generadores pseudoaleatorios fallan las reglas de validación del dominio."""
    pass


def linear_congruential(semilla: int, a: int, c: int, m: int, n: int) -> list[float]:
    """
    Genera una secuencia de números pseudoaleatorios en el intervalo [0, 1) usando el
    algoritmo del Generador Congruencial Lineal (LCG).

    Fórmula:
        X_{i+1} = (a * X_i + c) mod m
        R_i = X_i / m (normalizado a [0, 1))

    Parámetros:
        semilla (int): El valor inicial de la semilla X_0.
        a (int): La constante multiplicadora.
        c (int): La constante de incremento.
        m (int): La constante del módulo.
        n (int): La cantidad de números pseudoaleatorios a generar.

    Retorna:
        list[float]: Una lista de n números flotantes normalizados.
    """
    if m <= 0:
        raise GeneratorValidationError("El módulo 'm' debe ser mayor que 0.")
    if not (0 <= semilla < m):
        raise GeneratorValidationError(f"La semilla {semilla} debe estar en el rango [0, {m-1}].")
    if not (0 <= a < m):
        raise GeneratorValidationError(f"El multiplicador 'a' ({a}) debe estar en el rango [0, {m-1}].")
    if not (0 <= c < m):
        raise GeneratorValidationError(f"El incremento 'c' ({c}) debe estar en el rango [0, {m-1}].")
    if n < 0:
        raise GeneratorValidationError("La cantidad 'n' debe ser un entero no negativo.")

    results = []
    x = semilla
    for _ in range(n):
        x = (a * x + c) % m
        results.append(x / (m - 1))
    return results


def multiplicative_congruential(semilla: int, a: int, m: int, n: int) -> list[float]:
    """
    Genera una secuencia de números pseudoaleatorios en el intervalo [0, 1) usando el
    algoritmo del Generador Congruencial Multiplicativo (MCG).

    Fórmula:
        X_{i+1} = (a * X_i) mod m
        R_i = X_i / m (normalizado a [0, 1))

    Parámetros:
        semilla (int): El valor inicial de la semilla X_0. Debe ser coprimo y no nulo.
        a (int): La constante multiplicadora.
        m (int): La constante del módulo.
        n (int): La cantidad de números pseudoaleatorios a generar.

    Retorna:
        list[float]: Una lista de n números flotantes normalizados.
    """
    if m <= 0:
        raise GeneratorValidationError("El módulo 'm' debe ser mayor que 0.")
    if not (0 < semilla < m):
        raise GeneratorValidationError(f"La semilla {semilla} debe estar en el rango [1, {m-1}].")
    if not (0 <= a < m):
        raise GeneratorValidationError(f"El multiplicador 'a' ({a}) debe estar en el rango [0, {m-1}].")
    if n < 0:
        raise GeneratorValidationError("La cantidad 'n' debe ser un entero no negativo.")

    results = []
    x = semilla
    for _ in range(n):
        x = (a * x) % m
        results.append(x / (m-1))
    return results


def mid_square(semilla: int, n: int, digits: int = None) -> list[float]:
    """
    Genera una secuencia de números pseudoaleatorios en el intervalo [0, 1) usando el
    algoritmo de Cuadrados Medios (Mid-Square).

    Fórmula:
        X_{i+1} = Dígitos centrales 'd' de X_i^2
        R_i = X_i / 10^d

    Parámetros:
        semilla (int): El valor inicial de la semilla no negativa X_0.
        n (int): La cantidad de números pseudoaleatorios a generar.
        digits (int, opcional): La cantidad de dígitos (d) a usar (debe ser par).
                                Si no se especifica, se determina a partir de la longitud de la semilla.

    Retorna:
        list[float]: Una lista de n números flotantes normalizados.
    """
    if semilla < 0:
        raise GeneratorValidationError("La semilla debe ser un entero no negativo.")
    if n < 0:
        raise GeneratorValidationError("La cantidad 'n' debe ser un entero no negativo.")

    if digits is None:
        digits = len(str(semilla))

    if digits <= 0 or digits % 2 != 0:
        raise GeneratorValidationError(
            f"La cantidad de dígitos ({digits}) debe ser un entero positivo par."
        )

    max_value = 10 ** digits - 1
    if semilla > max_value:
        raise GeneratorValidationError(
            f"La semilla {semilla} excede el valor máximo para {digits} dígitos ({max_value})."
        )

    results = []
    x = semilla
    divisor = 10 ** digits

    for _ in range(n):
        squared = x ** 2
        squared_str = str(squared)
        
        # Si tiene menos dígitos que los requeridos, rellenamos con ceros a la izquierda
        if len(squared_str) < digits:
            squared_str = squared_str.zfill(digits)
            
        # Si la longitud es impar, añadimos un cero a la izquierda para hacerla par
        if len(squared_str) % 2 != 0:
            squared_str = "0" + squared_str
            
        # Extraer los dígitos centrales dinámicamente
        total_len = len(squared_str)
        start = (total_len - digits) // 2
        end = start + digits
        mid_str = squared_str[start:end]
        x = int(mid_str)
        results.append(x / divisor)

    return results


import math


def uniform_continuous(u_list: list[float], a: float, b: float) -> list[float]:
    """
    Transforma números U(0,1) a una Distribución Uniforme Continua U(a, b).
    Fórmula: X_i = a + (b - a) * U_i
    """
    if a >= b:
        raise GeneratorValidationError(f"El límite inferior 'a' ({a}) debe ser estrictamente menor que el límite superior 'b' ({b}).")
    
    return [a + (b - a) * u for u in u_list]


def exponential_continuous(u_list: list[float], lambd: float) -> list[float]:
    """
    Transforma números U(0,1) a una Distribución Exponencial con parámetro de tasa lambda.
    Fórmula: X_i = -1/lambda * ln(U_i)
    """
    if lambd <= 0:
        raise GeneratorValidationError(f"El parámetro lambda ({lambd}) debe ser estrictamente mayor que 0.")
    
    results = []
    for u in u_list:
        # Evitar logaritmo de 0
        u_safe = max(u, 1e-12)
        if u_safe >= 1.0:
            u_safe = 1.0 - 1e-12
        val = - (1.0 / lambd) * math.log(1.0 - u_safe)
        results.append(val)
    return results


def normal_continuous(u_list: list[float], mean: float, std_dev: float) -> list[float]:
    """
    Transforma números U(0,1) a una Distribución Normal N(mean, std_dev^2) usando la transformación Box-Muller.
    """
    if std_dev <= 0:
        raise GeneratorValidationError(f"La desviación estándar ({std_dev}) debe ser estrictamente mayor que 0.")
    
    results = []
    n = len(u_list)
    for i in range(0, n, 2):
        u1 = max(u_list[i], 1e-12)
        u2 = u_list[i+1] if (i + 1 < n) else u_list[0]
        
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
        
        results.append(mean + z0 * std_dev)
        if i + 1 < n:
            results.append(mean + z1 * std_dev)
            
    return results[:n]


def weibull_continuous(u_list: list[float], alpha: float, beta: float) -> list[float]:
    """
    Transforma números U(0,1) a una Distribución Weibull con parámetros de escala (alpha) y forma (beta).
    Fórmula: X_i = alpha * (-ln(1 - U_i))^(1/beta)
    """
    if alpha <= 0:
        raise GeneratorValidationError(f"El parámetro de escala alpha ({alpha}) debe ser mayor que 0.")
    if beta <= 0:
        raise GeneratorValidationError(f"El parámetro de forma beta ({beta}) debe ser mayor que 0.")
    
    results = []
    for u in u_list:
        u_safe = max(u, 1e-12)
        if u_safe >= 1.0:
            u_safe = 1.0 - 1e-12
        val = alpha * ((-math.log(1.0 - u_safe)) ** (1.0 / beta))
        results.append(val)
    return results
