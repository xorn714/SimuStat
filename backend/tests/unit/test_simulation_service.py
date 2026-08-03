# pyrefly: ignore [missing-import]
import pytest
from app.adapter.api.schema import SimulationRequest
from app.services.simulation_service import SimulationService
from app.domain.exceptions import GeneratorValidationError


def test_simulation_service_lcg_success():
    request = SimulationRequest(
        method="lcg",
        semilla=37,
        a=19,
        c=33,
        m=100,
        n=100,  # mayor que 2 para que corra las pruebas estadísticas
        alpha=0.05
    )
    response = SimulationService.run_simulation(request)
    assert len(response.numbers) == 100
    assert response.mean_test.statistic is not None
    assert response.variance_test.statistic is not None
    assert response.ks_test.statistic is not None


def test_simulation_service_missing_params():
    request = SimulationRequest(
        method="lcg",
        semilla=37,
        # faltan a, c, m
        n=10,
        alpha=0.05
    )
    with pytest.raises(GeneratorValidationError, match="se requieren los parámetros"):
        SimulationService.run_simulation(request)


def test_simulation_service_insufficient_n():
    request = SimulationRequest(
        method="lcg",
        semilla=37,
        a=19,
        c=33,
        m=100,
        n=1,  # menor que 2
        alpha=0.05
    )
    with pytest.raises(GeneratorValidationError, match="Se requieren generar al menos 2 números"):
        SimulationService.run_simulation(request)


def test_simulation_service_continuous_distribution_tests():
    # Distribución continua: las cuatro pruebas (media, varianza, KS y rachas)
    # se aplican también a la variable transformada y deben pasar
    request = SimulationRequest(
        method="mcg",
        semilla=42,
        a=48271,
        m=2**31 - 1,
        n=2000,
        alpha=0.05,
        distribution_type="continuous",
        distribution_name="normal",
        dist_params={"mean": 0.0, "std_dev": 1.0},
    )
    response = SimulationService.run_simulation(request)

    assert response.continuous_values is not None
    assert len(response.continuous_values) == 2000
    assert response.continuous_stats["theoretical_mean"] == 0.0
    assert response.distribution_tests is not None

    dist_tests = response.distribution_tests
    assert dist_tests.mean_test.passed is True
    assert dist_tests.variance_test.passed is True
    assert dist_tests.ks_test.passed is True
    assert dist_tests.streak_test.passed is True


def test_simulation_service_discrete_distribution_tests():
    # Distribución discreta: las cuatro pruebas (media, varianza, KS y rachas)
    # se aplican también a la variable transformada y deben pasar
    request = SimulationRequest(
        method="mcg",
        semilla=42,
        a=48271,
        m=2**31 - 1,
        n=2000,
        alpha=0.05,
        distribution_type="discrete",
        distribution_name="binomial",
        dist_params={"n": 10, "p": 0.5},
    )
    response = SimulationService.run_simulation(request)

    assert response.discrete_values is not None
    assert len(response.discrete_values) == 200
    assert response.discrete_stats.theoretical_mean == pytest.approx(5.0)
    assert response.discrete_stats.theoretical_variance == pytest.approx(2.5)
    assert response.discrete_histogram is not None
    assert len(response.discrete_histogram) >= 1

    dist_tests = response.distribution_tests
    assert dist_tests.mean_test.passed is True
    assert dist_tests.variance_test.passed is True
    assert dist_tests.ks_test.passed is True
    assert dist_tests.streak_test.passed is True


def test_simulation_service_continuous_backward_compatible():
    # El campo continuous_dist (usado por el frontend) sigue funcionando
    request = SimulationRequest(
        method="mcg",
        semilla=42,
        a=48271,
        m=2**31 - 1,
        n=2000,
        alpha=0.05,
        continuous_dist="exponential",
        dist_params={"lambd": 1.0},
    )
    response = SimulationService.run_simulation(request)

    assert len(response.continuous_values) == 2000
    assert response.continuous_stats is not None
    assert response.distribution_tests is not None
    assert response.distribution_tests.ks_test.statistic is not None


def test_simulation_service_discrete_not_enough_values():
    # n=5 números base y 10 ensayos por observación binomial => 0 observaciones
    request = SimulationRequest(
        method="mcg",
        semilla=42,
        a=48271,
        m=2**31 - 1,
        n=5,
        alpha=0.05,
        distribution_type="discrete",
        distribution_name="binomial",
        dist_params={"n": 10, "p": 0.5},
    )
    with pytest.raises(GeneratorValidationError, match="no contiene suficientes números"):
        SimulationService.run_simulation(request)


def test_simulation_service_unknown_distribution():
    request = SimulationRequest(
        method="mcg",
        semilla=42,
        a=48271,
        m=2**31 - 1,
        n=200,
        alpha=0.05,
        distribution_type="continuous",
        distribution_name="cauchy",
        dist_params={},
    )
    with pytest.raises(GeneratorValidationError, match="no soportada"):
        SimulationService.run_simulation(request)
