# pyrefly: ignore [missing-import]
import pytest
from app.domain.generators import (
    uniform_continuous,
    exponential_continuous,
    normal_continuous,
    weibull_continuous,
    GeneratorValidationError
)
from app.domain.continuous_stats import calculate_continuous_stats


def test_uniform_continuous():
    u_list = [0.0, 0.5, 1.0]
    res = uniform_continuous(u_list, 10.0, 20.0)
    assert res == [10.0, 15.0, 20.0]

    with pytest.raises(GeneratorValidationError):
        uniform_continuous(u_list, 20.0, 10.0)


def test_exponential_continuous():
    u_list = [0.0, 0.5]
    res = exponential_continuous(u_list, 0.5)
    assert len(res) == 2
    assert res[0] >= 0
    assert res[1] > 0

    with pytest.raises(GeneratorValidationError):
        exponential_continuous(u_list, -1.0)


def test_normal_continuous():
    u_list = [0.1, 0.9, 0.3, 0.7]
    res = normal_continuous(u_list, 0.0, 1.0)
    assert len(res) == 4

    with pytest.raises(GeneratorValidationError):
        normal_continuous(u_list, 0.0, 0.0)


def test_weibull_continuous():
    u_list = [0.2, 0.8]
    res = weibull_continuous(u_list, 1.5, 2.0)
    assert len(res) == 2

    with pytest.raises(GeneratorValidationError):
        weibull_continuous(u_list, -1.0, 2.0)


def test_calculate_continuous_stats():
    vals = [10.0, 12.0, 14.0, 16.0, 18.0]
    stats, hist = calculate_continuous_stats(vals, "uniform", {"a": 10.0, "b": 20.0})
    
    assert stats["empirical_mean"] == 14.0
    assert stats["theoretical_mean"] == 15.0
    assert "bins" in hist
    assert len(hist["bins"]) >= 5
