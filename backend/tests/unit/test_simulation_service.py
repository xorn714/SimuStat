# pyrefly: ignore [missing-import]
import pytest
from app.adapter.api.schema import SimulationRequest
from app.services.simulation_service import SimulationService
from app.domain.generators import GeneratorValidationError


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
