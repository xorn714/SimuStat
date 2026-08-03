# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
import numpy as np
from app.domain.validators import MeanTest, VarianceTest, KSTest, RunsTest


def test_mean_test():
    # Una muestra perfectamente centrada
    # Media = 0.5
    numbers = [0.1, 0.3, 0.5, 0.7, 0.9]
    limits, statistic, passed = MeanTest(0.05).test(numbers)
    assert passed is True
    assert 0.4 < statistic < 0.6
    assert limits[0] < statistic < limits[1]

    # Una muestra muy desviada
    numbers_bad = [0.01, 0.02, 0.03, 0.04, 0.05]
    _, _, passed_bad = MeanTest(0.05).test(numbers_bad)
    assert passed_bad is False


def test_variance_test():
    # Generar números uniformes estándar para probar
    np.random.seed(42)
    numbers = np.random.uniform(0, 1, 100).tolist()

    limits, statistic, passed = VarianceTest(0.05).test(numbers)
    # Debería pasar con un nivel de significancia del 5%
    assert passed is True
    assert limits[0] <= statistic <= limits[1]

    # Muestra con varianza extremadamente baja
    numbers_bad = [0.5] * 100
    _, _, passed_bad = VarianceTest(0.05).test(numbers_bad)
    assert passed_bad is False


def test_ks_test():
    # Muestra uniforme
    np.random.seed(42)
    numbers = np.random.uniform(0, 1, 100).tolist()

    limits, statistic, passed = KSTest(0.05).test(numbers)
    assert passed is True
    assert statistic < limits[1]

    # Muestra no uniforme (todos concentrados en un punto)
    numbers_bad = [0.1] * 100
    limits_bad, statistic_bad, passed_bad = KSTest(0.05).test(numbers_bad)
    assert passed_bad is False
    assert statistic_bad >= limits_bad[1]


def test_runs_test():
    # Una secuencia perfectamente alternada: 0.1 (<0.5), 0.9 (>=0.5), 0.2 (<0.5), 0.8 (>=0.5), etc.
    # Esto generará muchas rachas (demasiadas para ser aleatoria e independiente, por lo que NO pasa)
    numbers = [0.1, 0.9, 0.2, 0.8, 0.1, 0.9, 0.2, 0.8, 0.1, 0.9]
    limits, statistic, passed = RunsTest(0.05).test(numbers)
    assert passed is False

    # Secuencia uniforme aleatoria más larga (debería pasar)
    np.random.seed(42)
    numbers_ok = np.random.uniform(0, 1, 100).tolist()
    limits_ok, statistic_ok, passed_ok = RunsTest(0.05).test(numbers_ok)
    assert passed_ok is True
    assert limits_ok[0] <= statistic_ok <= limits_ok[1]

    # Secuencia no independiente (todos de un lado)
    numbers_bad = [0.1] * 10
    limits_bad, statistic_bad, passed_bad = RunsTest(0.05).test(numbers_bad)
    assert passed_bad is False
    assert statistic_bad == float('inf')


def test_mean_test_adapted_to_distribution():
    # Muestra Normal(10, 2²) simulada: media empírica cercana a 10
    np.random.seed(7)
    numbers = np.random.normal(10.0, 2.0, 500).tolist()
    limits, statistic, passed = MeanTest(
        0.05, expected_mean=10.0, expected_variance=4.0
    ).test(numbers)
    assert passed is True
    assert limits[0] <= statistic <= limits[1]

    # Muestra centrada en otro valor: debe fallar contra la media 10
    numbers_bad = np.random.normal(12.0, 2.0, 500).tolist()
    _, _, passed_bad = MeanTest(
        0.05, expected_mean=10.0, expected_variance=4.0
    ).test(numbers_bad)
    assert passed_bad is False


def test_variance_test_adapted_to_distribution():
    np.random.seed(7)
    numbers = np.random.normal(0.0, 3.0, 500).tolist()
    limits, statistic, passed = VarianceTest(0.05, expected_variance=9.0).test(numbers)
    assert passed is True
    assert limits[0] <= statistic <= limits[1]

    numbers_bad = np.random.normal(0.0, 5.0, 500).tolist()
    _, _, passed_bad = VarianceTest(0.05, expected_variance=9.0).test(numbers_bad)
    assert passed_bad is False


def test_ks_test_adapted_to_cdf():
    from scipy.stats import norm, expon
    from app.domain.stats import ContinuousStatsCalculator

    np.random.seed(7)
    numbers = np.random.exponential(scale=1.0, size=500).tolist()
    cdf = ContinuousStatsCalculator.get_cdf("exponential", {"lambd": 1.0})
    limits, statistic, passed = KSTest(0.05, cdf=cdf).test(numbers)
    assert passed is True
    assert statistic < limits[1]

    # Misma muestra probada contra una CDF normal: debe fallar
    bad_cdf = ContinuousStatsCalculator.get_cdf("normal", {"mean": 1.0, "std_dev": 1.0})
    _, _, passed_bad = KSTest(0.05, cdf=bad_cdf).test(numbers)
    assert passed_bad is False


def test_ks_test_discrete_with_pmf():
    from app.domain.generators import DiscreteDistributionGenerator
    from app.domain.stats import DiscreteStatsCalculator

    np.random.seed(42)
    u = np.random.uniform(0, 1, 5000).tolist()
    values = DiscreteDistributionGenerator.binomial(u, 15, 0.5)
    cdf = DiscreteStatsCalculator.get_cdf("binomial", {"n": 15, "p": 0.5})
    pmf = DiscreteStatsCalculator.get_pmf("binomial", {"n": 15, "p": 0.5})

    limits, statistic, passed = KSTest(0.05, cdf=cdf, pmf=pmf).test(values)
    assert passed is True
    assert statistic < limits[1]


def test_runs_test_adapted_threshold():
    # Muestra Bernoulli(0.5) con umbral en la media 0.5: pasa (independencia)
    np.random.seed(42)
    numbers = np.random.binomial(1, 0.5, 200).tolist()
    limits, statistic, passed = RunsTest(0.05, threshold=0.5).test(numbers)
    assert passed is True

    # Secuencia alternada de Bernoulli: demasiadas rachas => falla
    numbers_alt = [0, 1] * 50
    _, _, passed_alt = RunsTest(0.05, threshold=0.5).test(numbers_alt)
    assert passed_alt is False
