# pyrefly: ignore [missing-import]
import pytest
from app.domain.exceptions import GeneratorValidationError
from app.domain.generators import DiscreteDistributionGenerator


def test_bernoulli_deterministic():
    # u < p => éxito (1); en caso contrario 0
    assert DiscreteDistributionGenerator.bernoulli([0.0, 0.5, 0.9], 0.5) == [1, 0, 0]
    assert DiscreteDistributionGenerator.bernoulli([0.1, 0.7], 0.0) == [0, 0]
    assert DiscreteDistributionGenerator.bernoulli([0.1, 0.7], 1.0) == [1, 1]


def test_bernoulli_validation():
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.bernoulli([0.1, 0.7], -0.1)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.bernoulli([0.1, 0.7], 1.5)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.bernoulli([0.1, 1.2], 0.5)


def test_binomial_deterministic():
    # Bloques de n=4 uniformes; cuenta de éxitos (u < 0.5) por bloque
    u_list = [0.0, 0.4, 0.6, 1.0, 0.2, 0.8, 0.3, 0.7]
    assert DiscreteDistributionGenerator.binomial(u_list, 4, 0.5) == [2, 2]

    # p = 1.0 => todos los ensayos son éxitos
    assert DiscreteDistributionGenerator.binomial([0.1, 0.9, 0.5], 2, 1.0) == [2]

    # El último bloque incompleto se descarta
    assert DiscreteDistributionGenerator.binomial([0.1, 0.9], 3, 0.5) == []


def test_binomial_validation():
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.binomial([0.1, 0.9, 0.5], 0, 0.5)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.binomial([0.1, 0.9, 0.5], 3, 1.5)


def test_poisson_deterministic():
    # P(X=0) = e^-1 ≈ 0.3679; u=0.0 => X=0
    # u=0.9 => X=2 (0.9 supera la acumulada hasta k=1)
    assert DiscreteDistributionGenerator.poisson([0.0, 0.9], 1.0) == [0, 2]


def test_poisson_validation():
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.poisson([0.1, 0.9], 0.0)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.poisson([0.1, 0.9], -2.0)


def test_geometric_deterministic():
    # X = floor(ln(1-u) / ln(1-p))
    assert DiscreteDistributionGenerator.geometric([0.0, 0.5, 0.9], 0.5) == [0, 1, 3]


def test_geometric_validation():
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.geometric([0.1, 0.9], 0.0)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.geometric([0.1, 0.9], 1.5)


def test_negative_binomial_deterministic():
    # Suma de r=2 geométricas: geom(0.9, 0.5)=4 y geom(0.5, 0.5)=1 => total 5
    assert DiscreteDistributionGenerator.negative_binomial([0.9, 0.5], 2, 0.5) == [5]


def test_negative_binomial_validation():
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.negative_binomial([0.9, 0.5], 0, 0.5)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.negative_binomial([0.9, 0.5], 2, 0.0)


def test_hypergeometric_deterministic():
    # N=5, K=2, n=3 => X en [0, 2]
    # u < p_success en cada extracción sin reemplazo
    assert DiscreteDistributionGenerator.hypergeometric([0.1, 0.9, 0.9], 5, 2, 3) == [1]
    assert DiscreteDistributionGenerator.hypergeometric([0.1, 0.1, 0.1], 5, 2, 3) == [2]

    # El último bloque incompleto se descarta
    assert DiscreteDistributionGenerator.hypergeometric([0.1, 0.1], 5, 2, 3) == []


def test_hypergeometric_validation():
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.hypergeometric([0.1, 0.9], 0, 2, 3)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.hypergeometric([0.1, 0.9], 5, 7, 3)
    with pytest.raises(GeneratorValidationError):
        DiscreteDistributionGenerator.hypergeometric([0.1, 0.9], 5, 2, 8)
