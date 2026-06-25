# pyrefly: ignore [missing-import]
import re
# pyrefly: ignore [missing-import]
import pytest
from app.domain.generators import (
    linear_congruential,
    multiplicative_congruential,
    mid_square,
    GeneratorValidationError,
)


def test_linear_congruential_success():
    # Ejercicio sacado del libro de simulación y análisis de sistema con Promodel (2da edición)
    # Ejemplo 2.4 página 27
    # X_0 = 37, a = 19, c = 33, m = 100
    # X_1 = (19*37 + 33) % 100 = 736 % 100 = 36 => r_1 = 0.36
    # X_2 = (19*36 + 33) % 100 = 717 % 100 = 17 => r_2 = 0.17
    # X_3 = (19*17 + 33) % 100 = 356 % 100 = 56 => r_3 = 0.56
    # X_4 = (19*56 + 33) % 100 = 1109 % 100 = 97  => r_4 = 0.97
    results = linear_congruential(semilla=37, a=19, c=33, m=100, n=4)
    assert results == [0.36, 0.17, 0.56, 0.97]

    # Probar con n = 0
    results_empty = linear_congruential(semilla=37, a=19, c=33, m=100, n=0)
    assert results_empty == []


def test_linear_congruential_validation_errors():
    # Módulo <= 0
    with pytest.raises(GeneratorValidationError, match="El módulo 'm' debe ser mayor que 0"):
        linear_congruential(semilla=37, a=19, c=33, m=0, n=4)

    # Semilla fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        linear_congruential(semilla=100, a=19, c=33, m=100, n=4)
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        linear_congruential(semilla=-1, a=19, c=33, m=100, n=4)

    # Multiplicador 'a' fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        linear_congruential(semilla=37, a=100, c=33, m=100, n=4)
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        linear_congruential(semilla=37, a=-1, c=33, m=100, n=4)

    # Incremento 'c' fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="El incremento 'c' .* debe estar en el rango"):
        linear_congruential(semilla=37, a=19, c=50, m=50, n=4)
    with pytest.raises(GeneratorValidationError, match="El incremento 'c' .* debe estar en el rango"):
        linear_congruential(semilla=37, a=19, c=-1, m=100, n=4)

    # Cantidad 'n' negativa
    with pytest.raises(GeneratorValidationError, match="La cantidad 'n' debe ser un entero no negativo"):
        linear_congruential(semilla=37, a=19, c=33, m=100, n=-1)


def test_multiplicative_congruential_success():
    # Ejercicio sacado de Simulación: Un enfoque práctico (escrito por Raúl Coss Bu)
    # Tabla 2.4 en la página 27 del libro
    # X_0 = 17, a = 3, m = 100
    # X_1 = (3*17) % 100 = 51 => r_1 = 0.51
    # X_2 = (3*51) % 100 = 53 => r_2 = 0.53
    # X_3 = (3*53) % 100 = 59 => r_3 = 0.59
    # X_4 = (3*59) % 100 = 77 => r_4 = 0.77
    # X_5 = (3*77) % 100 = 31 => r_5 = 0.31
    results = multiplicative_congruential(semilla=17, a=3, m=100, n=5)
    expected = [0.51, 0.53, 0.59, 0.77, 0.31]
    assert len(results) == 5
    for r, e in zip(results, expected):
        assert pytest.approx(r) == e

    # Probar con n = 0
    results_empty = multiplicative_congruential(semilla=17, a=3, m=100, n=0)
    assert results_empty == []


def test_multiplicative_congruential_validation_errors():
    # Módulo <= 0
    with pytest.raises(GeneratorValidationError, match="El módulo 'm' debe ser mayor que 0"):
        multiplicative_congruential(semilla=17, a=3, m=0, n=5)

    # Semilla fuera de rango [1, m-1] (la semilla no puede ser 0 en MCG)
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        multiplicative_congruential(semilla=0, a=3, m=100, n=5)
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        multiplicative_congruential(semilla=100, a=3, m=100, n=5)

    # Multiplicador 'a' fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        multiplicative_congruential(semilla=17, a=100, m=100, n=5)
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        multiplicative_congruential(semilla=17, a=-1, m=100, n=5)

    # Cantidad 'n' negativa
    with pytest.raises(GeneratorValidationError, match="La cantidad 'n' debe ser un entero no negativo"):
        multiplicative_congruential(semilla=17, a=3, m=100, n=-1)


def test_mid_square_success():
    # Ejercicio sacado del libro de simulación y análisis de sistema con Promodel (2da edición)
    # Pagina 25 ejemplo 2.1
    # X_0 = 5735, d = 4
    # X_0^2 = 32890225 -> Dígitos medios: 8902 => r_1 = 0.8902
    # X_1^2 = 79245604 -> Dígitos medios: 2456 => r_2 = 0.2456
    # X_2^2 = 06031936 -> Dígitos medios: 0319 => r_3 = 0.0319
    # X_3^2 = 101761 -> Dígitos medios: 0176 => r_4 = 0.0176
    # X_4^2 = 030976 -> Dígitos medios: 3097 => r_5 = 0.3097
    results = mid_square(semilla=5735, n=5, digits=4)
    assert results == [0.8902, 0.2456, 0.0319, 0.0176, 0.3097]

    # Probar con dígitos = 2
    # X_0 = 45, d = 2
    # X_0^2 = 2025 -> Dígitos medios: 02 => r_1 = 0.02
    # X_1 = 2 -> X_1^2 = 4 (rellenado a 4 caracteres: 0004) -> Dígitos medios: 00 => r_2 = 0.00
    results_two_digits = mid_square(semilla=45, n=2, digits=2)
    assert results_two_digits == [0.02, 0.04]


def test_mid_square_validation_errors():
    # Semilla negativa
    with pytest.raises(GeneratorValidationError, match="La semilla debe ser un entero no negativo"):
        mid_square(semilla=-5, n=3)

    # Cantidad negativa
    with pytest.raises(GeneratorValidationError, match="La cantidad 'n' debe ser un entero no negativo"):
        mid_square(semilla=5772, n=-1)

    # Dígitos impares especificados
    with pytest.raises(GeneratorValidationError, match="debe ser un entero positivo par"):
        mid_square(semilla=5772, n=3, digits=3)

    # Dígitos impares autodetectados de la semilla
    with pytest.raises(GeneratorValidationError, match="debe ser un entero positivo par"):
        mid_square(semilla=123, n=3)

    # Semilla excede los dígitos máximos
    with pytest.raises(GeneratorValidationError, match="excede el valor máximo"):
        mid_square(semilla=1234, n=3, digits=2)
