# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
import numpy as np
from app.domain.validators import mean_test, variance_test, ks_test

def test_mean_test():
    # Una muestra perfectamente centrada
    # Media = 0.5
    numbers = [0.1, 0.3, 0.5, 0.7, 0.9]
    limits, statistic, passed = mean_test(numbers, 0.05)
    assert passed is True
    assert 0.4 < statistic < 0.6
    assert limits[0] < statistic < limits[1]

    # Una muestra muy desviada
    numbers_bad = [0.01, 0.02, 0.03, 0.04, 0.05]
    _, _, passed_bad = mean_test(numbers_bad, 0.05)
    assert passed_bad is False

def test_variance_test():
    # Generar números uniformes estándar para probar
    np.random.seed(42)
    numbers = np.random.uniform(0, 1, 100).tolist()
    
    limits, statistic, passed = variance_test(numbers, 0.05)
    # Debería pasar con un nivel de significancia del 5%
    assert passed is True
    assert limits[0] <= statistic <= limits[1]

    # Muestra con varianza extremadamente baja
    numbers_bad = [0.5] * 100
    _, _, passed_bad = variance_test(numbers_bad, 0.05)
    assert passed_bad is False

def test_ks_test():
    # Muestra uniforme
    np.random.seed(42)
    numbers = np.random.uniform(0, 1, 100).tolist()
    
    limits, statistic, passed = ks_test(numbers, 0.05)
    assert passed is True
    assert statistic < limits[1]

    # Muestra no uniforme (todos concentrados en un punto)
    numbers_bad = [0.1] * 100
    limits_bad, statistic_bad, passed_bad = ks_test(numbers_bad, 0.05)
    assert passed_bad is False
    assert statistic_bad >= limits_bad[1]
