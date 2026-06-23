# pyrefly: ignore [missing-import]
import pytest
from app.domain.generators import (
    linear_congruential,
    multiplicative_congruential,
    mid_square,
    GeneratorValidationError,
)


def test_linear_congruential_success():
    # Probar LCG con parámetros estándar
    # X_0 = 4, a = 5, c = 7, m = 8
    # X_1 = (5*4 + 7) % 8 = 3   => r_1 = 3/8 = 0.375
    # X_2 = (5*3 + 7) % 8 = 6   => r_2 = 6/8 = 0.75
    # X_3 = (5*6 + 7) % 8 = 5   => r_3 = 5/8 = 0.625
    # X_4 = (5*5 + 7) % 8 = 0   => r_4 = 0/8 = 0.0
    results = linear_congruential(semilla=4, a=5, c=7, m=8, n=4)
    assert results == [0.375, 0.75, 0.625, 0.0]

    # Probar con n = 0
    results_empty = linear_congruential(semilla=4, a=5, c=7, m=8, n=0)
    assert results_empty == []


def test_linear_congruential_validation_errors():
    # Módulo <= 0
    with pytest.raises(GeneratorValidationError, match="El módulo 'm' debe ser mayor que 0"):
        linear_congruential(semilla=4, a=5, c=7, m=0, n=4)

    # Semilla fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        linear_congruential(semilla=8, a=5, c=7, m=8, n=4)
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        linear_congruential(semilla=-1, a=5, c=7, m=8, n=4)

    # Multiplicador 'a' fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        linear_congruential(semilla=4, a=8, c=7, m=8, n=4)
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        linear_congruential(semilla=4, a=-1, c=7, m=8, n=4)

    # Incremento 'c' fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="El incremento 'c' .* debe estar en el rango"):
        linear_congruential(semilla=4, a=5, c=8, m=8, n=4)
    with pytest.raises(GeneratorValidationError, match="El incremento 'c' .* debe estar en el rango"):
        linear_congruential(semilla=4, a=5, c=-1, m=8, n=4)

    # Cantidad 'n' negativa
    with pytest.raises(GeneratorValidationError, match="La cantidad 'n' debe ser un entero no negativo"):
        linear_congruential(semilla=4, a=5, c=7, m=8, n=-1)


def test_multiplicative_congruential_success():
    # Probar MCG con parámetros estándar
    # X_0 = 5, a = 3, m = 7
    # X_1 = (3*5) % 7 = 1  => r_1 = 1/7
    # X_2 = (3*1) % 7 = 3  => r_2 = 3/7
    # X_3 = (3*3) % 7 = 2  => r_3 = 2/7
    # X_4 = (3*2) % 7 = 6  => r_4 = 6/7
    results = multiplicative_congruential(semilla=5, a=3, m=7, n=4)
    expected = [1/7, 3/7, 2/7, 6/7]
    assert len(results) == 4
    for r, e in zip(results, expected):
        assert pytest.approx(r) == e

    # Probar con n = 0
    results_empty = multiplicative_congruential(semilla=5, a=3, m=7, n=0)
    assert results_empty == []


def test_multiplicative_congruential_validation_errors():
    # Módulo <= 0
    with pytest.raises(GeneratorValidationError, match="El módulo 'm' debe ser mayor que 0"):
        multiplicative_congruential(semilla=5, a=3, m=0, n=4)

    # Semilla fuera de rango [1, m-1] (la semilla no puede ser 0 en MCG)
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        multiplicative_congruential(semilla=0, a=3, m=7, n=4)
    with pytest.raises(GeneratorValidationError, match="La semilla .* debe estar en el rango"):
        multiplicative_congruential(semilla=7, a=3, m=7, n=4)

    # Multiplicador 'a' fuera de rango [0, m-1]
    with pytest.raises(GeneratorValidationError, match="El multiplicador 'a' .* debe estar en el rango"):
        multiplicative_congruential(semilla=5, a=7, m=7, n=4)

    # Cantidad 'n' negativa
    with pytest.raises(GeneratorValidationError, match="La cantidad 'n' debe ser un entero no negativo"):
        multiplicative_congruential(semilla=5, a=3, m=7, n=-1)


def test_mid_square_success():
    # Probar Mid-Square con dígitos explícitos = 4
    # X_0 = 5772, d = 4
    # X_0^2 = 33315984 -> Dígitos medios: 3159 => r_1 = 0.3159
    # X_1^2 = 09979281 -> Dígitos medios: 9792 => r_2 = 0.9792
    # X_2^2 = 95883264 -> Dígitos medios: 8832 => r_3 = 0.8832
    results = mid_square(semilla=5772, n=3, digits=4)
    assert results == [0.3159, 0.9792, 0.8832]

    # Probar Mid-Square con dígitos autodectectados (la longitud de str(seed) es 4)
    results_auto = mid_square(semilla=5772, n=3)
    assert results_auto == [0.3159, 0.9792, 0.8832]

    # Probar con dígitos = 2
    # X_0 = 45, d = 2
    # X_0^2 = 2025 -> Dígitos medios: 02 => r_1 = 0.02
    # X_1 = 2 -> X_1^2 = 4 (rellenado a 4 caracteres: 0004) -> Dígitos medios: 00 => r_2 = 0.00
    results_two_digits = mid_square(semilla=45, n=2, digits=2)
    assert results_two_digits == [0.02, 0.00]


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
