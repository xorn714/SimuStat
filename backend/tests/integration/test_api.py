# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "¡Bienvenido a SimuStat API!" in response.json()["message"]


def test_generate_sequence_lcg_success():
    payload = {
        "method": "lcg",
        "semilla": 37,
        "a": 19,
        "c": 33,
        "m": 100,
        "n": 50,
        "alpha": 0.05
    }
    response = client.post("/api/v1/generate-sequence", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "numbers" in data
    assert len(data["numbers"]) == 50
    assert "mean_test" in data
    assert "variance_test" in data
    assert "ks_test" in data
    assert data["mean_test"]["passed"] in [True, False]


def test_generate_sequence_invalid_params():
    payload = {
        "method": "lcg",
        "semilla": 37,
        "a": 19,
        "c": 33,
        "m": 0,  # Inválido: m debe ser > 0
        "n": 50,
        "alpha": 0.05
    }
    response = client.post("/api/v1/generate-sequence", json=payload)
    # Pydantic validará la restricción del campo m > 0 (gt=0) y lanzará error de validación de request
    assert response.status_code == 422


def test_generate_sequence_discrete_distribution():
    payload = {
        "method": "mcg",
        "semilla": 42,
        "a": 48271,
        "m": 2**31 - 1,
        "n": 1000,
        "alpha": 0.05,
        "distribution_type": "discrete",
        "distribution_name": "poisson",
        "dist_params": {"lambda": 3.0},
    }
    response = client.post("/api/v1/generate-sequence", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "discrete_values" in data
    assert len(data["discrete_values"]) == 1000
    assert "discrete_stats" in data
    assert data["discrete_stats"]["theoretical_mean"] == 3.0
    assert "discrete_histogram" in data
    assert data["distribution_tests"]["ks_test"]["statistic"] is not None
    assert data["distribution_tests"]["streak_test"]["passed"] in [True, False]


def test_generate_sequence_continuous_distribution():
    payload = {
        "method": "mcg",
        "semilla": 42,
        "a": 48271,
        "m": 2**31 - 1,
        "n": 1000,
        "alpha": 0.05,
        "distribution_type": "continuous",
        "distribution_name": "uniform",
        "dist_params": {"a": 5.0, "b": 15.0},
    }
    response = client.post("/api/v1/generate-sequence", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "continuous_values" in data
    assert len(data["continuous_values"]) == 1000
    assert "distribution_tests" in data
    assert data["distribution_tests"]["mean_test"]["passed"] in [True, False]
    assert data["histogram"]["total_count"] == 1000
