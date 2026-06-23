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
        results.append(x / m)
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
        results.append(x / m)
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
    start = digits // 2
    end = start + digits

    for _ in range(n):
        squared = x ** 2
        # Rellenar con ceros a la izquierda hasta 2 * digits
        squared_str = str(squared).zfill(2 * digits)
        
        # Extraer los dígitos centrales
        mid_str = squared_str[start:end]
        x = int(mid_str)
        results.append(x / divisor)

    return results
